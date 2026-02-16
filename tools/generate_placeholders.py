import json
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

DATA_FILE = "assets/data/words.json"
IMAGES_DIR = "assets/images"

def get_color(text):
    # Generate a consistent pastel color from text
    hash_object = hashlib.md5(text.encode())
    hash_hex = hash_object.hexdigest()
    r = int(hash_hex[0:2], 16) % 127 + 128
    g = int(hash_hex[2:4], 16) % 127 + 128
    b = int(hash_hex[4:6], 16) % 127 + 128
    return (r, g, b)

def generate_icon(text, filename):
    size = 512
    img = Image.new('RGB', (size, size), color=get_color(text))
    d = ImageDraw.Draw(img)
    
    # Try to load a font
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    # Draw text in center
    # Calculate text size (rudimentary for default font, better for truetype)
    # For simplicity, just center roughly
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) / 2
    y = (size - text_height) / 2
    
    # Draw text (black for contrast)
    d.text((x, y), text, fill=(0, 0, 0), font=font)
    
    # Draw a border?
    d.rectangle([0, 0, size-1, size-1], outline=(0,0,0), width=5)

    filepath = os.path.join(IMAGES_DIR, filename)
    img.save(filepath)
    print(f"Generated {filepath}")

def main():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    for word in data['words']:
        # If icon missing, generate one
        if "icon" not in word or not word["icon"]:
             # Use text as filename basis
             clean_text = word["text"].lower().replace(" ", "_")
             filename = f"{clean_text}.png"
             
             generate_icon(word["text"], filename)
             word["icon"] = filename

    # Save updated json
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("Updated words.json with icon paths.")

if __name__ == "__main__":
    main()
