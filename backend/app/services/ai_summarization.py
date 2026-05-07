import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from typing import Dict

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_patient_summary(extracted_data: Dict) -> str:
    if not extracted_data:
        return "No specific data found."

    prompt = f"""
    You are 'MediAssist', a compassionate AI medical assistant. 
    Analyze these lab results and write 8-10 sentences.
    
    Results: {extracted_data}
    
    1. POSITIVE REINFORCEMENT: Start by highlighting all the NORMAL (Green) results.
    2. RISK ASSESSMENT: After the good news, identify any HIGH RISK values.
    3. LANGUAGE: Provide the response in the SAME language as the uploaded report.
    4. DISCLAIMER: State that this is an AI summary and not a final diagnosis.
    """

    # Try 1.5 Flash first, then fall back to Pro
    models_to_try = ['gemini-1.5-flash', 'gemini-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini {model_name} failed: {e}")
            continue

    return _generate_mental_health_fallback(extracted_data)

def _generate_mental_health_fallback(data: Dict) -> str:
    """Detailed fallback when AI is unavailable."""
    summary = "Hello! I am your MediAssist assistant. First, the good news: many of your levels look stable and healthy. "
    
    good = []
    risks = []
    
    # Common reference ranges (approximate for adult, general use)
    reference_ranges = {
        "Hemoglobin": {"min": 12.0, "max": 17.5, "unit": "g/dL"},
        "Cholesterol": {"min": 0, "max": 200, "unit": "mg/dL"},
        "Vitamin_D": {"min": 20.0, "max": 50.0, "unit": "ng/mL"},
        "Vitamin_B12": {"min": 200.0, "max": 900.0, "unit": "pg/mL"},
        "Glucose": {"min": 70.0, "max": 140.0, "unit": "mg/dL"},
        "Creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"}, # Kidney
        "SGPT": {"min": 7.0, "max": 56.0, "unit": "U/L"},       # Liver
        "SGOT": {"min": 8.0, "max": 45.0, "unit": "U/L"},       # Liver
        "TSH": {"min": 0.4, "max": 4.0, "unit": "mIU/L"},       # Thyroid
        "WBC": {"min": 4.5, "max": 11.0, "unit": "10^3/uL"},    # White Blood Cells
        "Platelets": {"min": 150.0, "max": 450.0, "unit": "10^3/uL"},
        "Sodium": {"min": 135.0, "max": 145.0, "unit": "mEq/L"},
        "Potassium": {"min": 3.5, "max": 5.0, "unit": "mEq/L"}
    }

    for k, v in data.items():
        clean_name = k.replace('_', ' ')
        try:
            val = float(v)
            if k in reference_ranges:
                ref = reference_ranges[k]
                if val < ref["min"]:
                    risks.append(f"{clean_name} (Low)")
                elif val > ref["max"]:
                    risks.append(f"{clean_name} (High)")
                else:
                    good.append(clean_name)
            else:
                # If we don't know the range, we don't assume it's good or bad to be safe.
                pass
        except:
            # If the value isn't a number (e.g. "Negative", "Clear"), we skip it for safety
            pass

    if good:
        summary += f"We are happy to see that your {', '.join(good)} are within expected ranges. This is a great sign! "
    if risks:
        summary += f"However, your {', '.join(risks)} require attention. Please discuss these with your doctor soon."
    
    return summary