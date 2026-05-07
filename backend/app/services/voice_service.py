import edge_tts
import uuid
import re
import base64
import io

def _convert_to_ssml(text: str, voice: str) -> str:
    """
    Converts plain text into SSML with natural pauses, 
    a warm speaking rate, and emphasis on key medical terms.
    """
    # Add pauses after periods and commas for natural breathing
    text = text.replace(". ", '.<break time="600ms"/> ')
    text = text.replace(", ", ',<break time="250ms"/> ')
    text = text.replace("? ", '?<break time="500ms"/> ')
    
    # Emphasize critical medical keywords
    keywords = ["Hemoglobin", "Cholesterol", "Vitamin D", "Vitamin B12",
                 "Creatinine", "Sodium", "Potassium", "doctor", "urgent",
                 "important", "risk", "healthy", "normal"]
    for word in keywords:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(f'<emphasis level="moderate">{word}</emphasis>', text)

    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
           xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="{voice}">
            <prosody rate="-10%" pitch="-2%" volume="loud">
                {text}
            </prosody>
        </voice>
    </speak>
    """.strip()
    return ssml


async def make_automated_call(phone_number: str, script: str):
    """
    Generates premium voice and returns it as Base64 — no file storage needed.
    """
    print(f"[LOG] Generating human-like voice for: {phone_number}")

    voice = "en-US-AvaMultilingualNeural"
    audio_base64 = None

    try:
        ssml_text = _convert_to_ssml(script, voice)
        communicate = edge_tts.Communicate(ssml_text, voice)
        
        # Collect audio chunks into memory instead of saving to disk
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
        status_msg = "Premium voice simulation complete."
    except Exception as e:
        print(f"[ERROR] SSML edge-tts failed: {e}")
        # Fallback: try without SSML
        try:
            communicate = edge_tts.Communicate(script, voice)
            audio_buffer = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
            status_msg = "Voice simulation complete."
        except Exception as e2:
            print(f"[ERROR] Fallback also failed: {e2}")
            status_msg = "Audio generation unavailable."

    return {
        "status": "success",
        "mode": "edge_premium_ssml",
        "audio_base64": audio_base64,
        "message": status_msg
    }