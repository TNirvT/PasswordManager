from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sys import platform
import base64
from os import remove, urandom
from shutil import copy2

def salt_gen():
    salt_new = urandom(16)
    with open(salt_path, "wb") as f:
        f.write(salt_new)

def key_write(key):
    with open(key_path, "wb") as f:     # wb = write bytes
        f.write(key)
    f.close()

def key_read():
    with open(key_path, "rb") as f:     # rb = read bytes
        key = f.read()
    f.close()
    return key

def key_random():
    key = Fernet.generate_key()
    return key

def key_pw(pw_for_keygen):
    password = pw_for_keygen.encode()
    with open(salt_path, "rb") as f:
        salt = f.read()
    f.close
    # salt = b'u\xbc\x17c\x8b\xff_\xc1\xc2go"\xa7\xa3}t'
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=101524,
            backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def file_encrypt(file_in, file_out, key, opt):
    with open(file_in, "rb") as f:   # Open the file to encrypt
        data = f.read()
    fernet = Fernet(key)
    if opt == "en":
        output = fernet.encrypt(data)
    elif opt == "de":
        output = fernet.decrypt(data)
    with open(file_out, "wb") as f: # Write the encrypted file
        f.write(output)

def str_encrypt(str_in, key, opt):
    fernet = Fernet(key)
    if opt == "en":
        str_out = fernet.encrypt(str_in.encode())
    elif opt == "de":
        str_out = fernet.decrypt(str_in).decode()
    return str_out

def master_pw(opt):
    while opt == "login":
        key = key_pw(input("Enter Master Password to continue: "))
        if key == key_read():
            print("Master Password correct!")
            break
        else:
            print("Incorrect password!")
            continue
    if opt == "new":
        key = key_pw(input("Create a new Master Password: "))
        key_write(key)
    elif opt == "change":
        pw_in = input("Enter a New Master Password: ")
        key = key_pw(pw_in)
        copy2(key_path, key_path+".old")
        key_write(key)
    elif opt == "del_old":
        remove(key_path+".old")

if platform.startswith("linux"):
    key_path = r"~/.keys/pwmngr.key"
elif platform.startswith("win32"):
    key_path = r"d:\py_prjs\.keys\pwmngr.key"
salt_path = key_path.replace("pwmngr.key", "pwmngr.salt")


# salt_gen()
# key_write(key_pw("pw123"))
# for i in range(10):
#     pw_test = "password"+str(i)
#     print(str_encrypt(pw_test, key_read(), "en"))
# s_enc = str_encrypt("testing123$|", key_read(), "en")
# print(s_enc)