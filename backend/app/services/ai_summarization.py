import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from typing import Dict

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("[WARNING] GEMINI_API_KEY is missing! Using fallback logic.")

def generate_patient_summary(extracted_data: Dict) -> str:
    """
    Generates a detailed medical summary using Gemini or a smart fallback.
    """
    if not extracted_data:
        return "We have received your report. However, no specific biomarkers were detected for analysis. Please consult your physician for a detailed review."

    # If API Key is missing, provide a "Smart" fallback that actually uses the data
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return _generate_smart_fallback(extracted_data)

    prompt = f"""
    You are 'MediAssist', a compassionate medical assistant. 
    Analyze these lab results and write a 8-10 sentences explanation for a patient.
    
    Results: {extracted_data}
    
    1. Be friendly.
    2. Explain the numbers simply.
    3. Suggest a small lifestyle tip.
    4. End with: 'Please discuss this with your doctor.'
    5. Do NOT give a medical diagnosis.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini Call Failed: {e}")
        return _generate_smart_fallback(extracted_data)

def _generate_smart_fallback(data: Dict) -> str:
    """Creates a detailed summary without needing an API key."""
    summary = "Hello! I've analyzed your results. "
    details = []
    for key, val in data.items():
        details.append(f"your {key.replace('_', ' ')} level was recorded at {val}")
    
    summary += "Specifically, " + ", and ".join(details) + ". "
    summary += "Overall, these results provide a good baseline. Please be sure to share this summary with your healthcare provider during your next visit."
    return summary