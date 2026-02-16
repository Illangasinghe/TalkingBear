import wave
import sys

def check_wav(filepath):
    try:
        with open(filepath, 'rb') as f:
            header = f.read(100)
            print(f"Header bytes: {header}")
            try:
                print(f"Header text: {header.decode('utf-8')}")
            except:
                print("Header text: (binary)")
            
        with wave.open(filepath, 'rb') as wf:
            # ... existing wave checks ...
            pass
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_wav(sys.argv[1])
    else:
        # Check a default file
        check_wav("assets/audio/frog.wav")
