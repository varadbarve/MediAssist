import fitz  # PyMuPDF
import re
from typing import Dict

def extract_medical_values_from_pdf(pdf_bytes: bytes) -> Dict:
    """
    Enhanced extraction logic to find common medical markers in PDF text.
    """
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {}

    # Define common medical markers and their regex patterns
    # We look for: [Marker Name] [Optional spaces/dots] [The Number]
    markers = {
        "Hemoglobin": [r"Hemoglobin", r"Hb"],
        "White_Blood_Cells": [r"WBC", r"White Blood Cells"],
        "Platelets": [r"Platelets", r"PLT"],
        "Glucose": [r"Glucose", r"Sugar", r"HbA1c"],
        "Cholesterol": [r"Cholesterol", r"Total Cholesterol"],
        "Vitamin_D": [r"Vitamin D", r"Vit D", r"25-OH Vitamin D"],
        "Vitamin_B12": [r"Vitamin B12", r"B12"],
        "Creatinine": [r"Creatinine"],
        "Thyroid_TSH": [r"TSH", r"Thyroid Stimulating Hormone"]
    }

    extracted_data = {}

    for label, patterns in markers.items():
        for pattern in patterns:
            # Regex: Pattern + optional characters like : or - + a number (decimal or int)
            # Example: "Hemoglobin: 14.5" or "Hb 12"
            regex = rf"{pattern}\s*[:\-]?\s*(\d+\.?\d*)"
            match = re.search(regex, text, re.IGNORECASE)
            if match:
                extracted_data[label] = match.group(1)
                break # Found this marker, move to the next one

    return extracted_data