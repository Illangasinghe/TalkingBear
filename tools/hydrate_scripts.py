import json
import os

WORDS_FILE = "assets/data/words.json"
SCRIPTS_FILE = "assets/data/scripts.json"

def main():
    if not os.path.exists(WORDS_FILE) or not os.path.exists(SCRIPTS_FILE):
        print("Data files missing.")
        return

    # Load words map
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    # Map text -> emoji
    word_map = {w['text']: w.get('emoji') for w in words_data['words']}

    # Load scripts
    with open(SCRIPTS_FILE, 'r', encoding='utf-8') as f:
        scripts_data = json.load(f)

    # Hydrate tiles
    for script in scripts_data['scripts']:
        for tile in script['tiles']:
            text = tile['text']
            # Remove icon if present
            if 'icon' in tile:
                del tile['icon']
                
            # If word map has emoji for this text, use it
            if text in word_map and word_map[text]:
                 tile['emoji'] = word_map[text]
            
    # Save scripts
    with open(SCRIPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=4, ensure_ascii=False)
        
    print("Updated scripts.json with emojis.")

if __name__ == "__main__":
    main()
