import fitz  # PyMuPDF
import re
from typing import Dict

def extract_medical_values_from_pdf(pdf_bytes: bytes) -> Dict:
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {}

    # Comprehensive list for Apollo Reports
    markers = {
        "Hemoglobin": [r"Hemoglobin", r"Hb"],
        "Cholesterol": [r"Cholesterol", r"Total Cholesterol"],
        "Creatinine": [r"CREATININE"],
        "Vitamin_D": [r"VITAMIN D", r"Vit D"],
        "Vitamin_B12": [r"VITAMIN B12", r"B12"],
        "Glucose": [r"Glucose", r"HbA1c", r"Sugar"],
        "Sodium": [r"SODIUM"],
        "Potassium": [r"POTASSIUM"],
        "Bilirubin": [r"BILIRUBIN, TOTAL"],
        "ALT_SGPT": [r"ALT/SGPT", r"ALANINE AMINOTRANSFERASE"],
        "AST_SGOT": [r"AST/SGOT", r"ASPARTATE AMINOTRANSFERASE"],
        "Uric_Acid": [r"URIC ACID"],
        "Calcium": [r"CALCIUM"]
    }

    extracted_data = {}
    for label, patterns in markers.items():
        for pattern in patterns:
            # Apollo reports often have the number on the NEXT line
            # This regex looks for the word followed by some noise, then the number
            regex = rf"{pattern}[\s\n]*[:\-]?[\s\n]*(\d+\.?\d*)"
            match = re.search(regex, text, re.IGNORECASE)
            if match:
                extracted_data[label] = match.group(1)
                break

    return extracted_data