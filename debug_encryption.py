
import os
import sys
import json
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Setup minimal Logging
logging.basicConfig(level=logging.DEBUG)

class MockDataManager:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.encryption_salt = base64.b64encode(os.urandom(16)).decode('utf-8')
        os.makedirs(config_dir, exist_ok=True)
        
    def _get_fernet(self, pin=None):
        if pin:
            print(f"DEBUG: Using PIN key with salt {self.encryption_salt}")
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=base64.b64decode(self.encryption_salt),
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(pin.encode()))
        else:
            print("DEBUG: Using Fallback key")
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'static_salt_for_obfuscation',
                iterations=1000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"default_obfuscation_key"))
        return Fernet(key)

    def save_and_load_test(self, pin=None):
        data = {"test": "valid"}
        json_str = json.dumps(data)
        
        # Encrypt
        fernet = self._get_fernet(pin)
        encrypted = fernet.encrypt(json_str.encode('utf-8'))
        print(f"Encrypted size: {len(encrypted)}")
        
        # Decrypt
        fernet2 = self._get_fernet(pin)
        decrypted = fernet2.decrypt(encrypted)
        print(f"Decrypted: {decrypted.decode('utf-8')}")
        
        assert json.loads(decrypted.decode('utf-8')) == data
        print("Test Passed!")

try:
    dm = MockDataManager("test_dir")
    print("--- Test 1: No PIN ---")
    dm.save_and_load_test(None)
    
    print("\n--- Test 2: With PIN ---")
    dm.save_and_load_test("1234")
    
except Exception as e:
    print(f"Test Failed: {e}")
    import traceback
    traceback.print_exc()
