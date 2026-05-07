import os
import edge_tts
import uuid
import re

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
        # Case-insensitive replacement with emphasis tags
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
    Generates premium, human-like voice using SSML and Edge-TTS.
    """
    print(f"[LOG] Generating human-like voice for: {phone_number}")

    output_dir = "temp_calls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_filename = f"call_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(output_dir, audio_filename)

    # One of Microsoft's most natural-sounding neural voices
    voice = "en-US-AvaMultilingualNeural"

    try:
        ssml_text = _convert_to_ssml(script, voice)
        communicate = edge_tts.Communicate(ssml_text, voice)
        await communicate.save(file_path)
        status_msg = "Premium voice simulation complete."
    except Exception as e:
        print(f"[ERROR] SSML edge-tts failed: {e}")
        # Fallback: try without SSML
        try:
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(file_path)
            status_msg = "Voice simulation complete."
        except Exception as e2:
            print(f"[ERROR] Fallback also failed: {e2}")
            status_msg = "Audio generation unavailable."
            audio_filename = None

    return {
        "status": "success",
        "mode": "edge_premium_ssml",
        "audio_file": audio_filename,
        "message": status_msg
    }