import requests
import json
import os
import time

TTS_URL = "http://localhost:5001/tts/generate"
OUTPUT_DIR = r"assets\audio"
DATA_DIR = r"assets\data"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_audio(text, filename, voice="af_nicole", output_dir=OUTPUT_DIR):
    """
    Generates audio for the given text and saves it to filename.
    """
    filepath = os.path.join(output_dir, filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        print(f"Skipping existing: {filename} in {output_dir}")
        return True

    payload = {
        "text": text,
        "voice": voice 
    }
    
    try:
        response = requests.post(TTS_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            # Check if response is JSON with base64
            try:
                data = response.json()
                if "audio_base64" in data:
                    import base64
                    audio_bytes = base64.b64decode(data["audio_base64"])
                    with open(filepath, "wb") as f:
                        f.write(audio_bytes)
                    print(f"Generated (base64 decoded): {filename} for '{text}'")
                    return True
            except:
                pass
            
            # Fallback for raw bytes
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Generated (raw): {filename} for '{text}'")
            return True
        else:
            print(f"Failed to generate '{text}': {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error generating '{text}': {e}")
        return False

import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate audio assets for TalkingBear")
    parser.add_argument("--voice", default="af_nicole", help="TTS voice ID (e.g. af_nicole, af_sarah)")
    parser.add_argument("--folder", default="whisper", help="Subfolder name inside assets/audio/")
    args = parser.parse_args()

    voice_id = args.voice
    target_dir = os.path.join(OUTPUT_DIR, args.folder)
    ensure_dir(target_dir)
    
    # 1. Load Scripts for phrases/fixed tiles
    scripts_path = os.path.join(DATA_DIR, "scripts.json")
    with open(scripts_path, 'r', encoding='utf-8') as f:
        scripts_data = json.load(f)
    
    # 2. Load Words for swappable items
    words_path = os.path.join(DATA_DIR, "words.json")
    with open(words_path, 'r', encoding='utf-8') as f:
        words_data = json.load(f)

    # Collect all unique text/audio pairs
    to_generate = {} # audio_filename -> text

    # From scripts
    for script in scripts_data['scripts']:
        for tile in script['tiles']:
            audio = tile.get('audio')
            text = tile.get('text')
            if audio and text:
                to_generate[audio] = text

    # From words
    for word in words_data['words']:
        audio = word.get('audio')
        text = word.get('text')
        if audio and text:
            to_generate[audio] = text

    print(f"Found {len(to_generate)} unique audio files to verify/generate.")
    
    count = 0
    for filename, text in to_generate.items():
        if generate_audio(text, filename, voice=voice_id, output_dir=target_dir):
            count += 1
            time.sleep(0.3)
    
    print(f"\nFinished. Successfully generated {count} files.")

if __name__ == "__main__":
    main()

