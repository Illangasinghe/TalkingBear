import json
import os

WORDS_FILE = "assets/data/words.json"

EMOJI_MAP = {
    "FROG": "🐸",
    "JAGUAR": "🐆",
    "BEAR": "🐻",
    "DOG": "🐶",
    "CAT": "🐱",
    "DINOSAUR": "🦕",
    "GHOST": "👻",
    "MOUSE": "🐭",
    "RIBBIT": "💬",
    "ROAR": "🦁",
    "GROWL": "🐻",
    "WOOF": "🐕",
    "MEOW": "🐈",
    "BOO": "👻",
    "CLOCK": "🕰️",
    "TREE": "🌳",
    "HOUSE": "🏠",
    "BED": "🛏️",
    "HILL": "⛰️",
    "SOFA": "🛋️",
    "POOL": "🏊",
    "MONKEYS": "🐒",
    "GHOSTS": "👻",
    "BEARS": "🐻",
    "DINOSAURS": "🦕",
    "WHAT DOES THE": "❓",
    "SAY": "🗣️",
    "THE": "👉",
    "CLIMBED UP": "🧗",
    "FIVE LITTLE": "5️⃣",
    "JUMPING ON": "🦘",
    "I WANT": "🍎",
    "APPLE": "🍎",
    "WATER": "💧",
    "BALL": "⚽",
    "BLOCKS": "🧱",
    "BOOK": "📚",
    "CRACKER": "🥨",
    "HUG": "🫂",
    "POTTY": "🚽",
    "OUTSIDE": "🌳",
    "I FEEL": "😊",
    "BECAUSE": "➡️",
    "HAPPY": "😊",
    "SAD": "😢",
    "ANGRY": "😡",
    "EXCITED": "🤩",
    "SCARED": "😨",
    "TIRED": "😴",
    "HUNGRY": "😋",
    "PLAYING": "🧸",
    "SLEEPING": "💤",
    "EATING": "🍎",
    "HURT": "🩹",
    "RAINING": "🌧️",
    "SUNNY": "☀️"
}

def main():
    if not os.path.exists(WORDS_FILE):
        print("Data file missing.")
        return

    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for word in data['words']:
        text_upper = word['text'].upper()
        
        # Remove old icon field if present
        if "icon" in word:
            del word["icon"]
            
        # Add emoji
        if text_upper in EMOJI_MAP:
            word["emoji"] = EMOJI_MAP[text_upper]
        else:
            # Fallback or leave empty? 
            # Try partial match or just leave it
            print(f"No emoji map for: {text_upper}")

    # Save updated json
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("Updated words.json with emojis.")

if __name__ == "__main__":
    main()
