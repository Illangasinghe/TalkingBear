import wave
import sys
import struct

def check_magnitude(filepath):
    try:
        with wave.open(filepath, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            
            # format 3 is float (4 bytes)
            if params.sampwidth == 4:
                # Unpack as floats
                count = len(frames) // 4
                floats = struct.unpack(f'{count}f', frames)
                max_val = max(abs(f) for f in floats)
                return max_val
            else:
                # Assume PCM
                if params.sampwidth == 2:
                    count = len(frames) // 2
                    shorts = struct.unpack(f'{count}h', frames)
                    return max(abs(s) for s in shorts) / 32768.0
                return 0.0
                
    except Exception as e:
        print(f"Error checking {filepath}: {e}")
        return 0.0

if __name__ == "__main__":
    for path in sys.argv[1:]:
        mag = check_magnitude(path)
        print(f"{path}: Magnitude {mag:.6f}")
