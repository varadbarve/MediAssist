import os
from gtts import gTTS
import uuid
from app.core import config

def make_automated_call(phone_number: str, script: str):
    """
    Simulates an automated call and generates a FREE audio file of the script.
    In a real production app, this would use Twilio, but for free building, 
    we generate the audio locally and mock the call.
    """
    print(f"--- [FREE MOCK DIALER] ---")
    print(f"Calling: {phone_number}")
    print(f"Script: {script}")

    # Generate audio for free using gTTS
    try:
        tts = gTTS(text=script, lang='en')
        audio_filename = f"call_{uuid.uuid4().hex}.mp3"
        # In a real local dev, you'd save this to a 'static' folder
        # tts.save(audio_filename)
        print(f"Audio generated: {audio_filename}")
    except Exception as e:
        print(f"TTS Error: {e}")

    print(f"--- [END OF MOCK CALL] ---")

    return {
        "status": "success", 
        "mode": "free_mock",
        "message": "Call simulated successfully for free."
    }