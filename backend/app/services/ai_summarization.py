from typing import Dict
from app.core import config
# In a real implementation, you would import the OpenAI library
# import openai

def generate_patient_summary(report_data: Dict) -> str:
    """
    Generates a patient-friendly summary of the medical report using an LLM.
    Follows strict safety rules from the PRD.
    """
    print("Generating AI summary...")

    # In a real implementation, you would use the openai client:
    # openai.api_key = config.OPENAI_API_KEY
    #
    # prompt = f"""
    # You are a helpful medical assistant. Your role is to explain medical report
    # results in simple, patient-friendly language.
    #
    # **SAFETY RULES:**
    # - DO NOT diagnose diseases.
    # - DO NOT prescribe new medicines.
    # - DO NOT override doctor advice.
    #
    # Explain these results simply: {report_data}
    # """
    # response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    # return response.choices[0].text.strip()

    # Dummy response based on PRD example for demonstration
    summary_parts = []
    if report_data.get("hemoglobin", 15) < 14: # Example normal value
        summary_parts.append("Your hemoglobin is lower than normal.")
    if report_data.get("vitamin_d", 30) < 30:
        summary_parts.append("Your Vitamin D levels are deficient.")
    if report_data.get("cholesterol", 200) > 200:
        summary_parts.append("Your cholesterol levels are elevated.")

    return " ".join(summary_parts) if summary_parts else "All values are within the normal range."