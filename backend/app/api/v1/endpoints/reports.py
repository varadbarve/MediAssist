from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services import report_processing, ai_summarization, voice_service

router = APIRouter()

@router.post("/upload")
async def upload_and_process_report(
    patient_id: str = Form(...),
    patient_phone_number: str = Form(...), # In a real app, fetch this from DB via patient_id
    file: UploadFile = File(...)
):
    """
    Endpoint to upload a PDF report, process it, generate a summary,
    and trigger an automated call. This simulates the main workflow from the PRD.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")

    # 1. Report Uploaded to System & AI Extracts Medical Values
    file_content = await file.read()
    extracted_data = report_processing.extract_medical_values_from_pdf(file_content)

    # In a real app, you would save the report and data to the database here.

    # 2. AI Generates Summary
    summary = ai_summarization.generate_patient_summary(extracted_data)

    # 3. Prescription & Doctor Notes Attached (simulated)
    # In a real app, you'd fetch this from the DB based on the report/patient.
    prescription_notes = "Take Vitamin D tablets once daily after breakfast. Avoid oily and spicy food for 5 days."
    
    full_script = f"Hello, this is a message from your clinic regarding your recent report. {summary}. Your doctor has prescribed the following: {prescription_notes}. To repeat this message, press 1. To speak to a staff member, press 3."

    # 4. Automated Call Initiated
    call_result = await voice_service.make_automated_call(
        phone_number=patient_phone_number, 
        script=full_script
    )

    return {
        "filename": file.filename,
        "extracted_data": extracted_data,
        "ai_summary": summary,
        "call_status": call_result
    }