import json
import os

WORDS_FILE = r"c:\dev\TalkingBear\assets\data\words.json"
SWAP_GROUPS_FILE = r"c:\dev\TalkingBear\assets\data\swap_groups.json"

VOCABULARY = {
    "A": ["APPLE", "ANT", "ALLIGATOR", "ARM", "AXE", "ANCHOR"],
    "B": ["BEAR", "BALL", "BIRD", "BANANA", "BOAT", "BUS"],
    "C": ["CAT", "CAR", "CAKE", "CUP", "COW", "CANDY"],
    "D": ["DOG", "DINOSAUR", "DUCK", "DOLL", "DRUM", "DESK"],
    "E": ["ELEPHANT", "EGG", "ELBOW", "EAGLE", "ENGINE", "EAR"],
    "F": ["FROG", "FISH", "FAN", "FORK", "FLOWER", "FIELD"],
    "G": ["GIRAFFE", "GOAT", "GRAPES", "GUITAR", "GLASS", "GATE"],
    "H": ["HAT", "HORSE", "HOUSE", "HAND", "HAMMER", "HILL"],
    "I": ["ICE CREAM", "IGLOO", "INSECT", "IRON", "ISLAND", "INK"],
    "J": ["JAGUAR", "JEEP", "JELLYFISH", "JAR", "JACKET", "JUMP"],
    "K": ["KITE", "KANGAROO", "KEY", "KING", "KITCHEN", "KNEE"],
    "L": ["LION", "LEAF", "LAMP", "LEMON", "LEG", "LADDER"],
    "M": ["MOUSE", "MOON", "MONKEY", "MASK", "MOUNTAIN", "MOUTH"],
    "N": ["NET", "NOSE", "NEST", "NECK", "NOTE", "NIGHT"],
    "O": ["OCTOPUS", "ORANGE", "OWL", "OVEN", "OCEAN", "OIL"],
    "P": ["PIG", "PUMPKIN", "PENCIL", "PIZZA", "PAN", "POT"],
    "Q": ["QUEEN", "QUILT", "QUESTION", "QUAIL", "QUARTER", "QUICK"],
    "R": ["RABBIT", "RAIN", "RING", "ROCKET", "ROAD", "RIVER"],
    "S": ["SUN", "SNAKE", "SHIP", "SHOE", "STAR", "SPOON"],
    "T": ["TIGER", "TREE", "TRAIN", "TABLE", "TRUCK", "TOY"],
    "U": ["UMBRELLA", "UNICORN", "UNDER", "UP", "UNCLE", "UNIT"],
    "V": ["VAN", "VASE", "VEGETABLE", "VINE", "VIOLIN", "VEST"],
    "W": ["WHALE", "WATCH", "WATER", "WIND", "WINDOW", "WHEEL"],
    "X": ["X-RAY", "XYLOPHONE", "XYGEN", "XEROX", "XYLYL", "XRAY"],
    "Y": ["YO-YO", "YAK", "YELLOW", "YARN", "YOGURT", "YEAR"],
    "Z": ["ZEBRA", "ZIPPER", "ZIGZAG", "ZERO", "ZOO", "ZONE"]
}

EMOJI_MAP = {
    "ANT": "🐜", "ALLIGATOR": "🐊", "ARM": "💪", "AXE": "🪓", "ANCHOR": "⚓",
    "BALL": "⚽", "BIRD": "🐦", "BANANA": "🍌", "BOAT": "⛵", "BUS": "🚌",
    "CAR": "🚗", "CAKE": "🍰", "CUP": "☕", "COW": "🐄", "CANDY": "🍬",
    "DUCK": "🦆", "DOLL": "🪆", "DRUM": "🥁", "DESK": "🖥️",
    "EGG": "🥚", "ELBOW": "💪", "EAGLE": "🦅", "ENGINE": "🚂", "EAR": "👂",
    "FISH": "🐟", "FAN": "🌬️", "FORK": "🍴", "FLOWER": "🌸", "FIELD": "🌱",
    "GOAT": "🐐", "GRAPES": "🍇", "GUITAR": "🎸", "GLASS": "🥛", "GATE": "⛩️",
    "HORSE": "🐎", "HAND": "✋", "HAMMER": "🔨",
    "IGLOO": "❄️", "INSECT": "🪲", "IRON": "⚡", "ISLAND": "🏝️", "INK": "🖋️",
    "JEEP": "🚙", "JELLYFISH": "🪼", "JAR": "🫙", "JACKET": "🧥", "JUMP": "🏃",
    "KANGAROO": "🦘", "KEY": "🔑", "KING": "👑", "KITCHEN": "🍳", "KNEE": "🦵",
    "LEAF": "🍃", "LAMP": "💡", "LEMON": "🍋", "LEG": "🦵", "LADDER": "🪜",
    "MOON": "🌙", "MONKEY": "🐒", "MASK": "🎭", "MOUNTAIN": "🏔️", "MOUTH": "👄",
    "NOSE": "👃", "NEST": "🪹", "NECK": "🧣", "NOTE": "🎵", "NIGHT": "🌃",
    "ORANGE": "🍊", "OWL": "🦉", "OVEN": "🍳", "OCEAN": "🌊", "OIL": "🛢️",
    "PUMPKIN": "🎃", "PENCIL": "✏️", "PIZZA": "🍕", "PAN": "🍳", "POT": "🍲",
    "QUILT": "🧵", "QUESTION": "❓", "QUAIL": "🐦", "QUARTER": "🪙", "QUICK": "⚡",
    "RAIN": "🌧️", "RING": "💍", "ROCKET": "🚀", "ROAD": "🛣️", "RIVER": "🏞️",
    "SNAKE": "🐍", "SHIP": "🚢", "SHOE": "👟", "STAR": "⭐", "SPOON": "🥄",
    "TRAIN": "🚂", "TABLE": "🪑", "TRUCK": "🚚", "TOY": "🧸",
    "UNICORN": "🦄", "UNDER": "⬇️", "UP": "⬆️", "UNCLE": "👨", "UNIT": "🔢",
    "VASE": "🏺", "VEGETABLE": "🥦", "VINE": "🌿", "VIOLIN": "🎻", "VEST": "🦺",
    "WATCH": "⌚", "WIND": "🌬️", "WINDOW": "🪟", "WHEEL": "🛞",
    "XYLOPHONE": "🎹", "XYGEN": "🧪", "XEROX": "📠", "XYLYL": "🧪", "XRAY": "🩻",
    "YAK": "🐂", "YELLOW": "💛", "YARN": "🧶", "YOGURT": "🍦", "YEAR": "📅",
    "ZIPPER": "🤐", "ZIGZAG": "📈", "ZERO": "0️⃣", "ZOO": "🦁", "ZONE": "📍"
}

def main():
    # Load words
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    
    existing_word_texts = {w['text'].upper() for w in words_data['words']}
    
    all_new_words = []
    for letter, words in VOCABULARY.items():
        for word_text in words:
            if word_text not in existing_word_texts:
                audio_filename = word_text.lower().replace(" ", "_").replace("-", "_") + ".wav"
                new_word = {
                    "text": word_text,
                    "audio": audio_filename,
                    "emoji": EMOJI_MAP.get(word_text, "")
                }
                words_data['words'].append(new_word)
                all_new_words.append(word_text)
            else:
                all_new_words.append(word_text)
    
    # Save updated words
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, indent=4, ensure_ascii=False)
    
    # Load swap groups
    with open(SWAP_GROUPS_FILE, 'r', encoding='utf-8') as f:
        swap_data = json.load(f)
    
    for group in swap_data['groups']:
        if group['id'] == 'alphabet_objects':
            # Add all vocabulary words to alphabet_objects, but avoid duplicates
            current_group_words = set(group['words'])
            for word_text in all_new_words:
                if word_text not in current_group_words:
                    group['words'].append(word_text)
            break
    
    # Save updated swap groups
    with open(SWAP_GROUPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(swap_data, f, indent=4, ensure_ascii=False)

    print(f"Added {len(all_new_words)} words to alphabet_objects.")

if __name__ == "__main__":
    main()
