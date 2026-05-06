import os
from gtts import gTTS
import uuid
from app.core import config

def make_automated_call(phone_number: str, script: str):
    """
    Simulates an automated call and generates a FREE audio file.
    The file is saved locally so you can hear the AI voice for free.
    """
    print(f"--- [FREE MOCK DIALER] ---")
    print(f"Calling: {phone_number}")
    print(f"Script: {script}")

    # Ensure the directory exists
    output_dir = "temp_calls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate audio for free using gTTS
    audio_filename = f"call_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(output_dir, audio_filename)
    
    try:
        tts = gTTS(text=script, lang='en')
        tts.save(file_path)
        print(f"✅ AI Voice saved to: backend/{file_path}")
    except Exception as e:
        print(f"TTS Error: {e}")

    print(f"--- [END OF MOCK CALL] ---")

    return {
        "status": "success", 
        "mode": "free_mock",
        "audio_file": audio_filename,
        "message": f"AI Voice generated successfully. Find it in backend/{output_dir}/"
    }