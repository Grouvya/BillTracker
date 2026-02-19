
import os

filepath = 'Billtracker_qt.py'
print(f"Repairing {filepath}...")

try:
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    print(f"Content length: {len(content)}")
    
    # Custom permissive encoder for Windows-1252 holes
    def permissive_windows1252_encode(text):
        bytes_list = []
        # Undefined bytes in Windows-1252:
        # 0x81, 0x8D, 0x8F, 0x90, 0x9D 
        holes = {0x81, 0x8D, 0x8F, 0x90, 0x9D}
        
        for i, char in enumerate(text):
            try:
                # Try standard cp1252
                b = char.encode('cp1252')
                bytes_list.append(b)
            except UnicodeEncodeError:
                # If encode fails, check if it's one of the "hole" characters
                # which PowerShell likely mapped from byte -> unicode control char
                code = ord(char)
                if code in holes:
                    bytes_list.append(bytes([code]))
                else:
                    # If it's some other unicode character that can't be encoded,
                    # like a real Emoji (U+1Fxxx), it implies successful decoding?
                    # But wait, if the file is Mojibake, real Emojis shouldn't exist as characters.
                    # They should be sequences of latin1/cp1252 chars.
                    # If we see a real Emoji, it means it survived corruption?
                    # Or it means my assumption about the file state is wrong.
                    # Let's log it but try to preserve it?
                    # No, if we can't encode it to cp1252, we can't 'reverse' the mojibake for it.
                    # We'll try latin1 fallback, or just skip?
                    # Latin1 maps 0-255. If code > 255, it fails.
                    print(f"Critical Error at pos {i}: Char {repr(char)} (U+{code:04X}) cannot be mapped.")
                    raise

        return b''.join(bytes_list)

    print("Attempting fix with permissive encoder...")
    try:
        fixed_bytes = permissive_windows1252_encode(content)
        fixed_content = fixed_bytes.decode('utf-8')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print("Success! Encoding repaired.")
        
    except Exception as ie:
        print(f"Encoding/Decoding failed in loop: {ie}")

except Exception as e:
    print(f"Repair Failed: {e}")
