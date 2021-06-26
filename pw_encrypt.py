from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64
import os
from shutil import copy2

# def salt_gen():
#     salt_new = os.urandom(16)
#     return salt_new

def key_write(key, key_file):
    with open(key_file, "wb") as f:     # wb = write bytes
        f.write(key)
    f.close()

def key_read(key_file):
    with open(key_file, "rb") as f:     # rb = read bytes
        key = f.read()
    f.close()
    return key

# def key_random():
#     key = Fernet.generate_key()
#     return key

def key_pw(pw_for_keygen):
    password = pw_for_keygen.encode()
    salt = b'u\xbc\x17c\x8b\xff_\xc1\xc2go"\xa7\xa3}t'
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

# def str_encrypt(str_in, key, opt):
#     fernet = Fernet(key)
#     if opt == "en":
#         str_out = fernet.encrypt(str_in.encode())
#     elif opt == "de":
#         str_out = fernet.decrypt(str_in).decode()
#     return str_out

def master_pw():
    while True:
        key = key_pw(input("Enter Master Password to continue: "))
        if key == key_read(key_path):
            print("Master Password correct!")
            if input("Press <enter> to continue, or <C> to change master password.") == "C":
                pw_in = input
                key = key_pw(pw_in)
                try:
                    copy2(key_path, key_path+".old")      # backup the key file, write or overwrite key.old
                except FileNotFoundError:
                    print("Old key is not found.")
                key_write(key, key_path)
                break # or return ???
            else: break
        else: print("Incorrect password!")
        
# def master_pw_ch():
#     if input("Press <enter> to continue, or <C> to change master password.") == "C":
#         pw_in = input
#         key = key_pw(pw_in)
#         try:
#             copy2(key_path, key_path+".old")      # backup the key file, write or overwrite key.old
#         except FileNotFoundError:
#             print("Old key is not found.")
#         key_write(key, key_path)
#     else: pass

key_path = r"d:\py_prjs\_keys\pwmngr.key"

# master_pw_ch("pw123")
