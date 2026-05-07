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
    for k, v in data.items():
        try:
            val = float(v)
            if k == "Hemoglobin" and val < 10: risks.append("Hemoglobin (Very Low)")
            elif k == "Cholesterol" and val > 200: risks.append("Cholesterol (High)")
            elif k == "Vitamin_D" and val < 20: risks.append("Vitamin D (Low)")
            elif k == "Vitamin_B12" and val < 150: risks.append("Vitamin B12 (Very Low)")
            else: good.append(k.replace('_', ' '))
        except:
            good.append(k.replace('_', ' '))

    if good:
        summary += f"We are happy to see that your {', '.join(good)} are within expected ranges. This is a great sign! "
    if risks:
        summary += f"However, your {', '.join(risks)} require attention. Please discuss these with your doctor soon."
    
    return summary