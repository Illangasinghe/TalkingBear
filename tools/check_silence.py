import wave
import sys
import struct

def is_silent(filepath):
    try:
        with wave.open(filepath, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            
            # format 3 is float (4 bytes)
            if params.sampwidth == 4:
                # We can just check if any byte is non-zero, though technically 
                # a non-zero float could be very close to zero.
                # But a truly silent file usually has all zero bytes in data chunk.
                return all(b == 0 for b in frames)
            elif params.sampwidth == 2:
                # 16-bit PCM
                return all(b == 0 for b in frames)
            else:
                return all(b == 0 for b in frames)
                
    except Exception as e:
        print(f"Error checking {filepath}: {e}")
        return True

if __name__ == "__main__":
    for path in sys.argv[1:]:
        silent = is_silent(path)
        print(f"{path}: {'SILENT' if silent else 'SOUND'}")
