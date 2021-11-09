import base64
from os import urandom
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MasterKey:
    def __init__(self, key_path: Path):
        self.key_path = key_path
        self.salt_path = key_path.parent / "pwmngr.salt"

    def exists(self):
        return Path(self.key_path).is_file() and Path(self.salt_path).is_file()

    def unlock(self, pw):
        with open(self.key_path, "rb") as f:     # rb = read bytes
            self.key = f.read()
        with open(self.salt_path, "rb") as f:     # rb = read bytes
            self.salt = f.read()

        valid = self.key == self.__pw_to_key(pw)
        if valid:
            self.fernet = Fernet(self.key)
        return valid

    def set_pw(self, pw):
        self.salt = urandom(16)
        with open(self.salt_path, "wb") as f:
            f.write(self.salt)

        self.key = self.__pw_to_key(pw)
        with open(self.key_path, "wb") as f:     # wb = write bytes
            f.write(self.key)

        self.fernet = Fernet(self.key)

    def encrypt(self, str):
        if self.fernet is None:
            raise Exception('MasterKey is not unlocked')
        return self.fernet.encrypt(str.encode())

    def decrypt(self, bytes):
        if self.fernet is None:
            raise Exception('MasterKey is not unlocked')
        return self.fernet.decrypt(bytes).decode()

    def __pw_to_key(self, pw):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=101524,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(pw.encode()))
