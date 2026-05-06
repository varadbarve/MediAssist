import google.generativeai as genai
from typing import Dict
from app.core import config

def generate_patient_summary(report_data: Dict) -> str:
    """
    Generates a patient-friendly summary using Google Gemini (Free Tier).
    """
    print("Generating AI summary with Gemini...")

    if not config.GEMINI_API_KEY:
        # Fallback to local rule-based logic if no API key is provided
        return _generate_fallback_summary(report_data)

    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are a helpful medical assistant. Explain these medical results in simple, 
        patient-friendly language. 
        
        **SAFETY RULES:**
        - DO NOT diagnose diseases.
        - DO NOT prescribe new medicines.
        - DO NOT override doctor advice.
        
        Results: {report_data}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return _generate_fallback_summary(report_data)

def _generate_fallback_summary(report_data: Dict) -> str:
    summary_parts = []
    if report_data.get("hemoglobin", 15) < 14:
        summary_parts.append("Your hemoglobin is lower than normal.")
    if report_data.get("vitamin_d", 30) < 30:
        summary_parts.append("Your Vitamin D levels are deficient.")
    if report_data.get("cholesterol", 200) > 200:
        summary_parts.append("Your cholesterol levels are elevated.")
    
    return " ".join(summary_parts) if summary_parts else "All values are within the normal range."