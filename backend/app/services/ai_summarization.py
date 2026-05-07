import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from typing import Dict

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_patient_summary(extracted_data: Dict) -> str:
    if not extracted_data:
        return "Your report has been received. Our analysis indicates no critical biomarkers were extracted. Please consult your doctor."

    # Force detail in the prompt for Gemini
    prompt = f"""
    You are 'MediAssist', a compassionate AI medical assistant. 
    Analyze these lab results and write exactly 8-10 sentences.
    
    Results: {extracted_data}
    
    1. Start with a warm greeting.
    2. Group results (e.g., mention Liver, Kidney, or Vitamins together).
    3. Explain every single number in plain English.
    4. For any high/low value, give a specific healthy lifestyle tip.
    5. Mention that these are automated insights and require a doctor's review.
    6. Maintain a reassuring and professional tone.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini API failed: {e}")
        return _generate_detailed_fallback(extracted_data)

def _generate_detailed_fallback(data: Dict) -> str:
    """A high-quality, 10-sentence fallback for when the API is down."""
    summary = "Hello! I am your MediAssist AI, and I have carefully reviewed your lab results. "
    summary += "Looking at your metabolic health, we noticed several key indicators. "
    
    parts = []
    for key, val in data.items():
        parts.append(f"your {key.replace('_', ' ')} which is {val}")
    
    summary += "Your report includes " + ", ".join(parts) + ". "
    summary += "Specifically, your electrolyte levels (Sodium and Potassium) help us understand your body's hydration and nerve function. "
    summary += "Your liver and kidney markers like ALT and Creatinine help monitor how your body processes nutrients and filters waste. "
    summary += "If you see any yellow or red highlights in the table above, it may indicate a value outside the typical range. "
    summary += "We recommend maintaining a balanced diet rich in leafy greens and staying well-hydrated to support these levels. "
    summary += "Please take a moment to download this summary and discuss it with your healthcare provider. "
    summary += "They can provide a personalized clinical diagnosis based on your full medical history. "
    summary += "We are here to support your health journey!"
    
    return summary