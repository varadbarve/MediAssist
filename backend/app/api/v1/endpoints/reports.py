from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services import report_processing, ai_summarization, voice_service

router = APIRouter()

@router.post("/upload")
async def upload_and_process_report(
    patient_id: str = Form(...),
    patient_phone_number: str = Form(...), 
    file: UploadFile = File(...)
):
    """
    Endpoint to upload a PDF report, process it, generate a summary,
    and trigger an automated call.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is supported.")

    # 1. Report Uploaded to System & AI Extracts Medical Values
    file_content = await file.read()
    extracted_data = report_processing.extract_medical_values_from_pdf(file_content)

    # 2. AI Generates Summary
    summary = ai_summarization.generate_patient_summary(extracted_data)

    # 3. Prescription & Doctor Notes Attached (simulated)
    prescription_notes = "Take Vitamin D tablets once daily after breakfast. Avoid oily and spicy food for 5 days."
    
    full_script = f"Hello, this is a message from your clinic regarding your recent report. {summary}. Your doctor has prescribed the following: {prescription_notes}. To repeat this message, press 1. To speak to a staff member, press 3."

    # DEVELOPER LOG: See the full script in your terminal
    print("\n" + "="*50)
    print("🚀 GENERATED CALL SCRIPT FOR DEVELOPER:")
    print(full_script)
    print("="*50 + "\n")

    # 4. Automated Call Initiated
    call_result = await voice_service.make_automated_call(
        phone_number=patient_phone_number, 
        script=full_script
    )

    return {
        "filename": file.filename,
        "extracted_data": extracted_data,
        "ai_summary": summary,
        "full_script": full_script,
        "call_status": call_result
    }