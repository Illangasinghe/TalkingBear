import json
import os

WORDS_FILE = r"c:\dev\TalkingBear\assets\data\words.json"
SWAP_GROUPS_FILE = r"c:\dev\TalkingBear\assets\data\swap_groups.json"
SCRIPTS_FILE = r"c:\dev\TalkingBear\assets\data\scripts.json"

NEW_VOCABULARY = {
    "People": ["MUM", "DAD", "BABY", "FRIEND", "TEACHER", "CHILD", "BOY", "GIRL", "FAMILY", "GRAN", "GRANDAD"],
    "School": ["SCHOOL", "CLASS", "PLAYGROUND", "BOOKBAG", "PENCIL", "RUBBER", "RULER", "GLUE", "SCISSORS", "LUNCHBOX", "DINNER", "SNACK"],
    "Home": ["HOME", "ROOM", "KITCHEN", "BATHROOM", "GARDEN", "DOOR", "WINDOW", "LIGHT", "TABLE", "CHAIR", "STAIRS"],
    "Body": ["HEAD", "HAIR", "EYES", "FACE", "HANDS", "FINGERS", "FEET", "TUMMY", "TOOTH", "NOSE", "COLD", "ILL", "MEDICINE", "PLASTER"],
    "Clothes": ["SHOES", "SOCKS", "COAT", "HAT", "JUMPER", "T-SHIRT", "TROUSERS", "DRESS", "PYJAMAS"],
    "Food": ["MILK", "JUICE", "TEA", "SANDWICH", "BREAD", "BUTTER", "CHEESE", "PASTA", "RICE", "CHICKEN", "CARROT", "PEAS", "BANANA", "BISCUIT"],
    "Transport_Places": ["PARK", "SHOP", "SUPERMARKET", "LIBRARY", "DOCTOR", "DENTIST", "BUS STOP", "STATION", "ROAD", "PAVEMENT", "CROSSING"],
    "Nature": ["CLOUD", "SKY", "WINDY", "SNOW", "PUDDLE", "LEAVES", "FLOWER", "GRASS", "MUD"],
    "Toys": ["TEDDY", "LEGO", "PUZZLE", "COLOURING", "PAINT", "BIKE", "SCOOTER", "SWING", "SLIDE", "FOOTBALL"],
    "Actions": ["GO", "STOP", "COME", "LOOK", "LISTEN", "HELP", "WAIT", "SHARE", "PLEASE", "THANK YOU", "SORRY"],
    "Describing": ["BIG", "SMALL", "LITTLE", "FAST", "SLOW", "WET", "DRY", "NICE", "FUNNY", "LOUD", "QUIET", "NEW", "OLD"],
    "Time": ["TODAY", "TOMORROW", "YESTERDAY", "MORNING", "NIGHT", "NOW", "LATER", "ONE", "TWO", "THREE", "FOUR", "FIVE", "TEN"]
}

EMOJI_MAP = {
    "MUM": "👩", "DAD": "👨", "BABY": "👶", "FRIEND": "👫", "TEACHER": "👩‍🏫", "CHILD": "🧒", "BOY": "👦", "GIRL": "👧", "FAMILY": "👨‍👩‍👧‍👦", "GRAN": "👵", "GRANDAD": "👴",
    "SCHOOL": "🏫", "CLASS": "🏫", "PLAYGROUND": "🛝", "BOOKBAG": "🎒", "PENCIL": "✏️", "RUBBER": "🧼", "RULER": "📏", "GLUE": "🧪", "SCISSORS": "✂️", "LUNCHBOX": "🍱", "DINNER": "🍽️", "SNACK": "🍿",
    "HOME": "🏠", "ROOM": "🏠", "KITCHEN": "🍳", "BATHROOM": "🛀", "GARDEN": "🪴", "DOOR": "🚪", "WINDOW": "🪟", "LIGHT": "💡", "TABLE": "🪑", "CHAIR": "🪑", "STAIRS": "🪜",
    "HEAD": "🙆", "HAIR": "💇", "EYES": "👁️", "FACE": "👤", "HANDS": "🙌", "FINGERS": "🖐️", "FEET": "🦶", "TUMMY": "🤰", "TOOTH": "🦷", "NOSE": "👃", "COLD": "🤒", "ILL": "🤢", "MEDICINE": "💊", "PLASTER": "🩹",
    "SHOES": "👟", "SOCKS": "🧦", "COAT": "🧥", "HAT": "🎩", "JUMPER": "🧶", "T-SHIRT": "👕", "TROUSERS": "👖", "DRESS": "👗", "PYJAMAS": "🛌",
    "MILK": "🥛", "JUICE": "🍹", "TEA": "☕", "SANDWICH": "🥪", "BREAD": "🍞", "BUTTER": "🧈", "CHEESE": "🧀", "PASTA": "🍝", "RICE": "🍚", "CHICKEN": "🍗", "CARROT": "🥕", "PEAS": "🫛", "BANANA": "🍌", "BISCUIT": "🍪",
    "PARK": "🌳", "SHOP": "🛍️", "SUPERMARKET": "🛒", "LIBRARY": "📚", "DOCTOR": "🩺", "DENTIST": "🦷", "BUS STOP": "🚏", "STATION": "🚉", "ROAD": "🛣️", "PAVEMENT": "🚶", "CROSSING": "🚶",
    "CLOUD": "☁️", "SKY": "🌌", "WINDY": "🌬️", "SNOW": "❄️", "PUDDLE": "💧", "LEAVES": "🍃", "FLOWER": "🌸", "GRASS": "🌱", "MUD": "💩",
    "TEDDY": "🧸", "LEGO": "🧱", "PUZZLE": "🧩", "COLOURING": "🖍️", "PAINT": "🎨", "BIKE": "🚲", "SCOOTER": "🛴", "SWING": "🛝", "SLIDE": "🛝", "FOOTBALL": "⚽",
    "GO": "🏃", "STOP": "🛑", "COME": "👋", "LOOK": "👀", "LISTEN": "👂", "HELP": "🆘", "WAIT": "⏳", "SHARE": "🤝", "PLEASE": "🙏", "THANK YOU": "🙌", "SORRY": "😔",
    "BIG": "🐘", "SMALL": "🐭", "LITTLE": "🐜", "FAST": "🏎️", "SLOW": "🐌", "WET": "🌧️", "DRY": "☀️", "NICE": "😊", "FUNNY": "😂", "LOUD": "📢", "QUIET": "🤫", "NEW": "✨", "OLD": "👴",
    "TODAY": "📅", "TOMORROW": "⏭️", "YESTERDAY": "⏮️", "MORNING": "🌅", "NIGHT": "🌃", "NOW": "⏱️", "LATER": "⌛", "ONE": "1️⃣", "TWO": "2️⃣", "THREE": "3️⃣", "FOUR": "4️⃣", "FIVE": "5️⃣", "TEN": "🔟"
}

def main():
    # Load data
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    with open(SWAP_GROUPS_FILE, 'r', encoding='utf-8') as f:
        swap_data = json.load(f)
    with open(SCRIPTS_FILE, 'r', encoding='utf-8') as f:
        scripts_data = json.load(f)

    existing_word_texts = {w['text'].upper() for w in words_data['words']}

    # 1. Add Words
    for cat, words in NEW_VOCABULARY.items():
        for word_text in words:
            if word_text not in existing_word_texts:
                audio_filename = word_text.lower().replace(" ", "_").replace("-", "_") + ".wav"
                new_word = {
                    "text": word_text,
                    "audio": audio_filename,
                    "emoji": EMOJI_MAP.get(word_text, "")
                }
                words_data['words'].append(new_word)
                existing_word_texts.add(word_text)

    # 2. Add Swap Groups
    existing_group_ids = {g['id'] for g in swap_data['groups']}
    for cat, words in NEW_VOCABULARY.items():
        group_id = cat.lower()
        if group_id not in existing_group_ids:
            swap_data['groups'].append({
                "id": group_id,
                "words": words
            })
        else:
            # Update existing group
            for group in swap_data['groups']:
                if group['id'] == group_id:
                    current_tokens = set(group['words'])
                    for w in words:
                        if w not in current_tokens:
                            group['words'].append(w)
                    break

    # 3. Add Strategic Scripts
    NEW_SCRIPTS = [
        {
            "id": "daily_routine_script",
            "title": "Daily Routine",
            "tiles": [
                {"id": "dr1", "text": "TODAY IS", "type": "fixed", "audio": "today_is.wav"},
                {"id": "dr2", "text": "MORNING", "type": "swappable", "swap_group": "time", "audio": "morning.wav", "emoji": "🌅"},
                {"id": "dr3", "text": "I AM", "type": "fixed", "audio": "i_am.wav"},
                {"id": "dr4", "text": "GO", "type": "swappable", "swap_group": "actions", "audio": "go.wav", "emoji": "🏃"},
                {"id": "dr5", "text": "TO", "type": "fixed", "audio": "to.wav"},
                {"id": "dr6", "text": "SCHOOL", "type": "swappable", "swap_group": "school", "audio": "school.wav", "emoji": "🏫"}
            ]
        },
        {
            "id": "my_clothes_script",
            "title": "My Clothes",
            "tiles": [
                {"id": "c1", "text": "I NEED MY", "type": "fixed", "audio": "i_need_my.wav"},
                {"id": "c2", "text": "SHOES", "type": "swappable", "swap_group": "clothes", "audio": "shoes.wav", "emoji": "👟"},
                {"id": "c3", "text": "FOR", "type": "fixed", "audio": "for.wav"},
                {"id": "c4", "text": "OUTSIDE", "type": "swappable", "swap_group": "transport_places", "audio": "outside.wav", "emoji": "🌳"}
            ]
        },
        {
            "id": "my_body_script",
            "title": "My Body",
            "tiles": [
                {"id": "b1", "text": "MY", "type": "fixed", "audio": "my.wav"},
                {"id": "b2", "text": "HEAD", "type": "swappable", "swap_group": "body", "audio": "head.wav", "emoji": "🙆"},
                {"id": "b3", "text": "FEELS", "type": "fixed", "audio": "feels.wav"},
                {"id": "b4", "text": "COLD", "type": "swappable", "swap_group": "describing", "audio": "cold.wav", "emoji": "🤒"}
            ]
        }
    ]

    for ns in NEW_SCRIPTS:
        if not any(s['id'] == ns['id'] for s in scripts_data['scripts']):
            scripts_data['scripts'].append(ns)
            # Add implicit words for fixed tiles if missing
            for tile in ns['tiles']:
                if tile['type'] == 'fixed' and tile['text'] not in existing_word_texts:
                    words_data['words'].append({
                        "text": tile['text'],
                        "audio": tile['audio']
                    })
                    existing_word_texts.add(tile['text'])

    # Save data
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(words_data, f, indent=4, ensure_ascii=False)
    with open(SWAP_GROUPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(swap_data, f, indent=4, ensure_ascii=False)
    with open(SCRIPTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(scripts_data, f, indent=4, ensure_ascii=False)

    print("UK Expansion complete.")

if __name__ == "__main__":
    main()
