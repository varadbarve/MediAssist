"""
Layer 4 — Input Validation & Sanitization
Validates and sanitizes all user inputs before processing.
Prevents injection attacks, malicious file uploads, and garbage data.
"""

import re
from fastapi import HTTPException, UploadFile


# --- Constants ---
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
PDF_MAGIC_BYTES = b"%PDF"
PATIENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9\-]{1,50}$")
# E.164 format: + followed by 10-15 digits
PHONE_PATTERN = re.compile(r"^\+[1-9]\d{9,14}$")


def validate_patient_id(patient_id: str) -> str:
    """Validate patient ID format (alphanumeric + hyphens, max 50 chars)."""
    patient_id = patient_id.strip()
    if not PATIENT_ID_PATTERN.match(patient_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid patient ID. Must be alphanumeric with hyphens, max 50 characters."
        )
    return patient_id


def validate_phone_number(phone_number: str) -> str:
    """Validate phone number in E.164 format (+<country_code><number>)."""
    phone_number = phone_number.strip()
    if not PHONE_PATTERN.match(phone_number):
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number. Must be in E.164 format (e.g., +919876543210)."
        )
    return phone_number


async def validate_pdf_file(file: UploadFile) -> bytes:
    """
    Validate uploaded file is a genuine PDF within size limits.
    Returns the file content bytes if valid.
    """
    # Check declared content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF is supported."
        )

    # Read file content
    file_content = await file.read()

    # Check file size
    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB."
        )

    # Check empty file
    if len(file_content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Verify PDF magic bytes (file signature)
    if not file_content[:4].startswith(PDF_MAGIC_BYTES):
        raise HTTPException(
            status_code=400,
            detail="File does not appear to be a valid PDF (invalid file signature)."
        )

    return file_content


def sanitize_extracted_data(data: dict) -> dict:
    """
    Sanitize extracted medical values before passing to AI.
    Strips any non-numeric content that could be prompt injection attempts.
    """
    sanitized = {}
    for key, value in data.items():
        # Only allow clean alphanumeric key names
        clean_key = re.sub(r"[^a-zA-Z0-9_]", "", str(key))
        if not clean_key:
            continue

        # Only allow numeric values (with optional decimal point)
        clean_value = str(value).strip()
        if re.match(r"^\d+\.?\d*$", clean_value):
            sanitized[clean_key] = clean_value
        else:
            # For non-numeric values (like "Negative", "Clear"), keep only
            # alphabetical characters — strip anything that looks like instructions
            alpha_only = re.sub(r"[^a-zA-Z\s\.]", "", clean_value)
            if alpha_only and len(alpha_only) < 50:  # Reasonable length for a lab value
                sanitized[clean_key] = alpha_only

    return sanitized
