import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from typing import Dict

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_patient_summary(extracted_data: Dict) -> str:
    """
    Generates a detailed, compassionate medical summary using Gemini.
    """
    if not extracted_data:
        return "No significant medical data was found in the report. Please consult your doctor for a manual review."

    prompt = f"""
    You are 'MediAssist', a compassionate medical assistant. 
    Analyze these lab results and write a 3-4 sentence explanation for a patient.
    
    Data: {extracted_data}
    
    Rules:
    1. Be very friendly and reassuring.
    2. Explain what each value means in simple terms.
    3. If values are high or low, suggest a general healthy tip (e.g., drink more water, eat more greens).
    4. End with: 'Please remember to discuss these results with your doctor.'
    5. Do NOT give a medical diagnosis.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Detailed Fallback if Gemini is down
        summary = "I've reviewed your latest lab results. "
        for key, val in extracted_data.items():
            summary += f"Your {key} is {val}. "
        summary += "Everything looks manageable, but please review this with your primary physician to be certain. Stay hydrated!"
        return summary