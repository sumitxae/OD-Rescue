from cryptography.fernet import Fernet
from ..config.config import Config

class EncryptionHelper:
    def __init__(self, key: bytes = None):
        """
        Initialize with a key. Generate a new key if not provided.
        """
        self.key = Config.ENCRYPTION_KEY.encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, content: str) -> str:
        """
        Encrypts a given string.
        """
        return self.cipher.encrypt(content.encode()).decode()

    def decrypt(self, encrypted_content: str) -> str:
        """
        Decrypts a given string.
        """
        return self.cipher.decrypt(encrypted_content.encode()).decode()
    
helper = EncryptionHelper()