import fitz  # PyMuPDF
import re
from typing import Dict

def extract_medical_values_from_pdf(file_content: bytes) -> Dict:
    """
    Extracts key medical values from a PDF report using PyMuPDF and Regex.
    This is a FREE and LOCAL process.
    """
    print("Reading PDF content...")
    
    # Open the PDF from bytes
    doc = fitz.open(stream=file_content, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    print("Extracted Text Sample:", full_text[:200]) # For debugging

    # Search for specific markers using Regular Expressions
    # Look for the word, followed by some spaces/chars, and then a number
    extracted_data = {
        "hemoglobin": _find_value(r"Hemoglobin.*?(\d+\.?\d*)", full_text),
        "cholesterol": _find_value(r"Cholesterol.*?(\d+\.?\d*)", full_text),
        "vitamin_d": _find_value(r"Vitamin D.*?(\d+\.?\d*)", full_text),
        "sugar": _find_value(r"(?:Glucose|Sugar).*?(\d+\.?\d*)", full_text),
    }

    # Remove any None values to keep the data clean
    return {k: v for k, v in extracted_data.items() if v is not None}

def _find_value(pattern: str, text: str):
    """Helper to find a numeric value in text using a regex pattern."""
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None