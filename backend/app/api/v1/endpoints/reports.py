"""
Reports endpoint — Protected with:
- Layer 3: Rate limiting (5/min)
- Layer 4: Input validation & sanitization
- Layer 6: Audit logging
- Layer 9: JWT authentication required
"""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.models.patient import Patient
from app.models.report import Report
from app.models.prescription import Prescription
from app.services import report_processing, ai_summarization, voice_service
from app.services.auth_service import get_current_user
from app.core.rate_limiter import limiter
from app.core.validators import validate_patient_id, validate_phone_number, validate_pdf_file, sanitize_extracted_data
from app.core.audit import log_event

router = APIRouter()


@router.post("/upload")
@limiter.limit("5/minute")
async def upload_and_process_report(
    request: Request,
    patient_id: str = Form(...),
    patient_phone_number: str = Form(...),
    prescription_notes: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint to upload a PDF report, process it, generate a summary,
    save results to database, and trigger an automated call.
    Requires authentication (JWT Bearer token).
    """
    client_ip = request.client.host if request.client else "unknown"

    # --- Layer 4: Input Validation ---
    patient_id = validate_patient_id(patient_id)
    patient_phone_number = validate_phone_number(patient_phone_number)
    file_content = await validate_pdf_file(file)

    # Log the upload event
    log_event(
        event_type="REPORT_UPLOAD",
        action="upload_started",
        ip_address=client_ip,
        patient_id=patient_id,
        user_email=current_user.email,
        details=f"File: {file.filename}, Size: {len(file_content)} bytes"
    )

    # 1. Report Uploaded to System & AI Extracts Medical Values
    extracted_data = report_processing.extract_medical_values_from_pdf(file_content)

    # --- Layer 4: Sanitize extracted data before AI processing ---
    extracted_data = sanitize_extracted_data(extracted_data)

    # 2. AI Generates Summary
    summary = ai_summarization.generate_patient_summary(extracted_data)

    log_event(
        event_type="AI_SUMMARY",
        action="summary_generated",
        ip_address=client_ip,
        patient_id=patient_id,
        user_email=current_user.email,
        details=f"Summary length: {len(summary)} chars"
    )

    # 3. Database Persistence Logic
    # Generate deterministic UUID from custom patient ID to fit schema
    uuid_id = uuid.uuid5(uuid.NAMESPACE_DNS, patient_id)
    try:
        # Check if patient exists, create if not
        db_patient = db.query(Patient).filter(Patient.patient_id == uuid_id).first()
        if not db_patient:
            db_patient = Patient(patient_id=uuid_id, age_group="adult", gender="unknown")
            db_patient.set_phone(patient_phone_number)
            db.add(db_patient)
            db.flush()

        # Parse extracted markers to save in report table
        hemoglobin_val = None
        if "Hemoglobin" in extracted_data:
            try:
                hemoglobin_val = float(extracted_data["Hemoglobin"])
            except ValueError:
                pass

        cholesterol_val = None
        if "Cholesterol" in extracted_data:
            try:
                cholesterol_val = float(extracted_data["Cholesterol"])
            except ValueError:
                pass

        vitamin_d_val = None
        if "Vitamin_D" in extracted_data:
            try:
                vitamin_d_val = float(extracted_data["Vitamin_D"])
            except ValueError:
                pass

        db_report = Report(
            patient_id=uuid_id,
            hemoglobin=hemoglobin_val,
            cholesterol=cholesterol_val,
            vitamin_d=vitamin_d_val
        )
        db.add(db_report)
        db.flush()

        # Create prescription record using doctor-supplied notes
        db_prescription = Prescription(
            patient_id=uuid_id,
            medicine_name=prescription_notes,
            dosage="As prescribed",
            timing="See notes"
        )
        db.add(db_prescription)
        db.commit()
    except Exception as db_err:
        db.rollback()
        print(f"[DATABASE ERROR] Failed to save clinical records: {db_err}")
        raise HTTPException(
            status_code=500,
            detail="Failed to save report and prescription data to database."
        )

    full_script = f"Hello, this is a message from your clinic regarding your recent report. {summary}. Your doctor has prescribed the following: {prescription_notes}. To repeat this message, press 1. To speak to a staff member, press 3."

    # DEVELOPER LOG: See the full script in your terminal
    print("\n" + "=" * 50)
    print("GENERATED CALL SCRIPT FOR DEVELOPER:")
    print(full_script)
    print("=" * 50 + "\n")

    # 4. Automated Call Initiated
    call_result = await voice_service.make_automated_call(
        phone_number=patient_phone_number,
        script=full_script
    )

    log_event(
        event_type="CALL",
        action="call_initiated",
        ip_address=client_ip,
        patient_id=patient_id,
        user_email=current_user.email,
        details=f"Phone: ***{patient_phone_number[-4:]}, Status: {call_result.get('status', 'unknown')}"
    )

    return {
        "filename": file.filename,
        "extracted_data": extracted_data,
        "ai_summary": summary,
        "full_script": full_script,
        "call_status": call_result
    }