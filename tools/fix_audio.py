import requests
import os
import base64

TTS_URL = "http://localhost:5001/tts/generate"

def test_generate(text, filename, voice):
    payload = {"text": text, "voice": voice}
    try:
        response = requests.post(TTS_URL, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "audio_base64" in data:
                audio_bytes = base64.b64decode(data["audio_base64"])
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"Generated {filename} for '{text}' with {voice}")
                return True
        print(f"Failed {text} with {voice}: {response.status_code}")
    except Exception as e:
        print(f"Error {text} with {voice}: {e}")
    return False

if __name__ == "__main__":
    test_generate("TOILET", r"assets\audio\default\toilet.wav", "af_sarah")
    test_generate("BISCUIT", r"assets\audio\default\biscuit.wav", "af_sarah")
    test_generate("TOILET", r"assets\audio\whisper\toilet.wav", "af_bella")
    test_generate("BISCUIT", r"assets\audio\whisper\biscuit.wav", "af_bella")
