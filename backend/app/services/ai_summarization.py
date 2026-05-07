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
    
    CRITICAL INSTRUCTIONS:
    1. POSITIVE REINFORCEMENT: Start by highlighting all the NORMAL (Green) results. Congratulate the patient on these.
    2. RISK ASSESSMENT: After the good news, identify any HIGH RISK or DANGEROUS values. Explain why they are important.
    3. TONE: Be reassuring, clear, and empathetic.
    4. LANGUAGE: Provide the response in the SAME language as the uploaded report.
    5. CALL TO ACTION: Suggest a specific healthy tip for the risks and insist on a doctor visit.
    6. DISCLAIMER: State that this is an AI summary and not a final diagnosis.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini API failed: {e}")
        return _generate_mental_health_fallback(extracted_data)

def _generate_mental_health_fallback(data: Dict) -> str:
    """A detailed fallback that prioritizes mental well-being and risk awareness."""
    summary = "Hello! I am your MediAssist assistant. First, the good news: many of your levels look stable and healthy. "
    
    # Simple logic to group good vs bad for the fallback
    good = []
    risks = []
    for k, v in data.items():
        val = float(v)
        if k == "Hemoglobin" and val < 10: risks.append("Hemoglobin (Very Low)")
        elif k == "Cholesterol" and val > 200: risks.append("Cholesterol (High)")
        elif k == "Vitamin_D" and val < 20: risks.append("Vitamin D (Low)")
        elif k == "Vitamin_B12" and val < 150: risks.append("Vitamin B12 (Very Low)")
        else: good.append(k.replace('_', ' '))

    if good:
        summary += f"We are happy to see that your {', '.join(good)} are within expected ranges. This is a great sign of overall health! "
    
    if risks:
        summary += f"However, we noticed that your {', '.join(risks)} require closer attention. These are important markers for your energy and heart health. "
        summary += "We strongly recommend scheduling a follow-up with your doctor this week to discuss these specific values. "
    
    summary += "In the meantime, focus on a balanced diet and rest. Remember, this is just an automated summary to help you prepare for your doctor's visit. Stay positive!"
    return summary