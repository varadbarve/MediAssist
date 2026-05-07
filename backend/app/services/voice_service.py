import os
from gtts import gTTS
import uuid
from app.core import config

def make_automated_call(phone_number: str, script: str):
    """
    Simulates an automated call and generates a FREE audio file.
    """
    # Internal logging (only shows in your terminal/Render logs)
    print(f"[LOG] Generating voice for: {phone_number}")

    output_dir = "temp_calls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_filename = f"call_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(output_dir, audio_filename)
    
    try:
        tts = gTTS(text=script, lang='en')
        tts.save(file_path)
        status_msg = "Voice simulation complete."
    except Exception as e:
        print(f"[ERROR] TTS Failed: {e}")
        status_msg = "Audio generation unavailable."
        audio_filename = None

    return {
        "status": "success", 
        "mode": "free_mock",
        "audio_file": audio_filename,
        "message": status_msg # This is what the user sees
    }