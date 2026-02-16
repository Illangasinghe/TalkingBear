import json
import os

WORDS_FILE = r"c:\dev\TalkingBear\assets\data\words.json"
SWAP_GROUPS_FILE = r"c:\dev\TalkingBear\assets\data\swap_groups.json"
SCRIPTS_FILE = r"c:\dev\TalkingBear\assets\data\scripts.json"

LOCALIZATION_MAP = {
    "CANDY": ("SWEETS", "sweets.wav", "🍬"),
    "CRACKER": ("BISCUIT", "biscuit.wav", "🍪"),
    "TRUCK": ("LORRY", "lorry.wav", "🚛"),
    "YOGURT": ("YOGHURT", "yoghurt.wav", "🍦"),
    "POTTY": ("TOILET", "toilet.wav", "🚽"),
    "POOL": ("SWIMMING POOL", "swimming_pool.wav", "🏊"),
    "JEEP": ("JELLY", "jelly.wav", "🫙"),
    "XYGEN": (None, None, None),
    "XYLYL": (None, None, None),
    "XEROX": (None, None, None),
}

X_WORDS_MAP = {
    "AXE": "🪓",
    "BOX": "📦",
    "FOX": "🦊",
    "TAXI": "🚕",
    "SIX": "6️⃣",
    "MIX": "🥣",
}

def main():
    # 1. Load data
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    with open(SWAP_GROUPS_FILE, 'r', encoding='utf-8') as f:
        swap_data = json.load(f)
    with open(SCRIPTS_FILE, 'r', encoding='utf-8') as f:
        scripts_data = json.load(f)

    # 2. Process Words
    new_words = []
    removed_words = set(LOCALIZATION_MAP.keys())
    
    # Track word mapping for group/script updates
    word_rename_map = {}
    for old, info in LOCALIZATION_MAP.items():
        if info[0]:
            word_rename_map[old] = info[0]

    for word in words_data['words']:
        text_upper = word['text'].upper()
        
        if text_upper in LOCALIZATION_MAP:
            new_text, new_audio, new_emoji = LOCALIZATION_MAP[text_upper]
            if new_text:
                word['text'] = new_text
                word['audio'] = new_audio
                word['emoji'] = new_emoji
                new_words.append(word)
            else:
                # Removed word
                continue
        elif text_upper == "XRAY": # Case specific fix
            word['text'] = "X-RAY"
            word['audio'] = "x_ray.wav"
            word_rename_map["XRAY"] = "X-RAY"
            new_words.append(word)
        elif text_upper == "X-RAY":
            new_words.append(word)
        else:
            new_words.append(word)

    # Add new X words if not present
    existing_texts = {w['text'].upper() for w in new_words}
    for x_text, x_emoji in X_WORDS_MAP.items():
        if x_text not in existing_texts:
            new_words.append({
                "text": x_text,
                "audio": x_text.lower() + ".wav",
                "emoji": x_emoji
            })

    words_data['words'] = new_words

    # 3. Update Swap Groups
    for group in swap_data['groups']:
        updated_words = []
        for word in group['words']:
            if word.upper() in word_rename_map:
                new_name = word_rename_map[word.upper()]
                if new_name not in updated_words:
                    updated_words.append(new_name)
            elif word.upper() in removed_words:
                continue
            else:
                if word not in updated_words:
                    updated_words.append(word)
        
        # Special case for 'X' in alphabet_objects
        if group['id'] == 'alphabet_objects':
            # Remove old ones
            # (already covered by word_rename_map/removed_words logic)
            # Ensure new X words are there
            for x_text in X_WORDS_MAP:
                if x_text not in updated_words:
                    updated_words.append(x_text)
                    
        group['words'] = updated_words

    # 4. Update Scripts
    for script in scripts_data['scripts']:
        for tile in script['tiles']:
            if 'text' in tile:
                text_upper = tile['text'].upper()
                if text_upper in word_rename_map:
                    new_text = word_rename_map[text_upper]
                    tile['text'] = new_text
                    # Also update audio/emoji if they match the word's defaults
                    for word in words_data['words']:
                        if word['text'].upper() == new_text.upper():
                            tile['audio'] = word['audio']
                            if 'emoji' in word:
                                tile['emoji'] = word['emoji']
                            break

    # 5. Save back
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, indent=4, ensure_ascii=False)
    with open(SWAP_GROUPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(swap_data, f, indent=4, ensure_ascii=False)
    with open(SCRIPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=4, ensure_ascii=False)

    print("Localization complete.")

if __name__ == "__main__":
    main()
