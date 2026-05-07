import os
import edge_tts
import uuid

async def make_automated_call(phone_number: str, script: str):
    """
    Asynchronous premium voice generation.
    """
    print(f"[LOG] Generating premium voice for: {phone_number}")

    output_dir = "temp_calls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_filename = f"call_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(output_dir, audio_filename)
    
    # Professional female voice
    voice = "en-IN-NeerjaNeural" 

    try:
        communicate = edge_tts.Communicate(script, voice)
        await communicate.save(file_path)
        status_msg = "Premium voice simulation complete."
    except Exception as e:
        print(f"[ERROR] edge-tts Failed: {e}")
        status_msg = "Audio generation unavailable."
        audio_filename = None

    return {
        "status": "success", 
        "mode": "edge_premium",
        "audio_file": audio_filename,
        "message": status_msg
    }