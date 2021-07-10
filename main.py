# Built-in
import argparse
import os
import traceback
from getpass import getpass
from shutil import copy2
from sys import platform

# PIP
import pyperclip
import tldextract
import sqlite3
from cryptography.fernet import Fernet

# Project
from pw_gen import pwgen, pwgen_custom
from master_key import MasterKey

if platform.startswith("win32"):
    db_path = os.path.abspath(" /../../.database/pwmngr.db")
    key_path = os.path.abspath(" /../../.keys/pwmngr.key")
else:
    db_path = os.path.expanduser("~/.database/pwmngr.db")
    key_path = os.path.expanduser("~/.keys/pwmngr.key")

master_key = MasterKey(key_path)
conn = sqlite3.connect(db_path)

parse = argparse.ArgumentParser()
parse.add_argument("--debug", action="store_true", help="Insert test data table to debug database.")
args = parse.parse_args()

#######################################
### data for debug only ###
def insert_debug_data():
    db_path = "pwmngr_debug.db"
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS pwtable (
        url text,
        login text,
        remark text,
        password blob
        )
    """)
    def inserts_db(list_in):
        curs = conn.cursor()
        curs.executemany("INSERT INTO pwtable VALUES (?,?,?,?)", list_in)
        conn.commit()

    list1 = [
        ("abc.com", "name@email.com", "", master_key.encrypt("pw_test1")),
        ("testing.com", "name@email.com", "hahaha", master_key.encrypt("pw_test2")),
        ("school.org", "myidno", "some notes", master_key.encrypt("pw_test3")),
    ]
    inserts_db(list1)

#######################################

def unlock_master_key():
    while True:
        pw = getpass("Enter Master Password to continue: ")
        if master_key.unlock(pw):
            print("Master Password correct!")
            break
        else:
            print("Incorrect password!")
            continue

def create_master_key():
    pw = getpass("Create a new Master Password: ")
    master_key.set_pw(pw)

def change_master_pw():
    pw = getpass("Enter a new Master Password: ")
    master_key.set_pw(pw)

#######################################

def insert_db(url_in, login_in, remark_in, pw_in):
    curs = conn.cursor()
    curs.execute("INSERT INTO pwtable VALUES (?,?,?,?)", (url_in, login_in, remark_in, pw_in))
    conn.commit()

def search_db(url_in):
    curs = conn.cursor()
    curs.execute("SELECT login, remark, password FROM pwtable WHERE url = (?)", (url_in,))
    row = curs.fetchone()
    conn.commit()
    if not row:
        return None
    else:
        return {"login":row[0], "re":row[1], "pw":master_key.decrypt(row[2])}

def update_db(url_in, data_in, opt):
    curs = conn.cursor()
    if opt == "pw":
        curs.execute("UPDATE pwtable SET password = (?) WHERE url = (?)", (data_in, url_in))
    elif opt == "log":
        curs.execute("UPDATE pwtable SET login = (?) WHERE url = (?)", (data_in, url_in))
    elif opt == "re":
        curs.execute("UPDATE pwtable SET remark = (?) WHERE url = (?)", (data_in, url_in))
    conn.commit()

def new_entry(domain):
    user_opt = input(f"New web site detected: {domain}\n(1)Create new entry, (Otherwise)Search again. ==> ")
    if user_opt == "1":
        new_login = input(f"Login id/email for {domain}: ")
        new_remark = input(f"Additional note: ")
        new_pw = pwgen()
        pyperclip.copy(new_pw)
        new_pw_enc = master_key.encrypt(new_pw)
        insert_db(domain, new_login, new_remark, new_pw_enc)
        print(f"New entry created for {domain}\nLogin & Password are: {new_login}:|  {new_pw}  | Password copied to clipboard!")

def update_retrieve(s_result):
    print(f"Record found. Login ID: {s_result['login']}  (Note: {s_result['re']}).")
    user_opt = input("(1)Retrieve password (2)Generate new password (3)OR custom password (4)Update database Login ID and note ==> ")
    if user_opt == "1":
        pyperclip.copy(s_result["pw"])
        print("Password copied to clipboard!")
    elif user_opt == "2" or user_opt == "3":
        if user_opt == "2": new_pw = pwgen()
        else: new_pw = pwgen_custom(input("Input the symbols allowed: "))
        new_pw_enc = master_key.encrypt(new_pw)
        update_db(domain, new_pw_enc, "pw")
        pyperclip.copy(new_pw)
        print(f"Password for {domain} (Note: {s_result['re']}) updated and copied to clipboard!\nLogin & Password are: {s_result['login']}:|  {new_pw}  |")
    elif user_opt == "4":
        update_input = input("Input new Login ID and note (separated by ';'): ")
        if update_input != "":
            update_in = update_input.split(";", 1)
            update_db(domain, update_in[0].strip(), "log")
            if update_in[1]: update_db(domain, update_in[1].strip(), "re")
            print(f"Database updated for {domain} (Note: {search_db(domain)['re']}), Login ID: {search_db(domain)['login']}")
    else:
        print("Error, please enter 1, 2 or 3.")


print("***Python Password Manager***")

if master_key.exists():
    unlock_master_key()
else:
    create_master_key()

if args.debug:
    insert_debug_data()

curs = conn.cursor()
curs.execute("SELECT count(name) FROM sqlite_master WHERE type= 'table' AND name='pwtable' ")
if curs.fetchone()[0] == 0:
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS pwtable (
        url text,
        login text,
        remark text,
        password blob
        )
    """)
    conn.commit()
else:
    if input("Press <enter> to continue, or <Ch> to change master password: ") == "Ch":
        # Make sure DB is unused before touching the file
        conn.close()
        copy2(db_path, db_path+".old")
        
        conn = sqlite3.connect(db_path+".old")
        curs = conn.cursor()
        curs.execute("SELECT url, password FROM pwtable")
        all_rows = curs.fetchall()
        conn.close()

        all_dec = []
        for row in all_rows:  # don't use 'i' for non-integer loop variable
            data_dec = master_key.decrypt(row[1])
            all_dec.append((row[0], data_dec))  # cannot modify i, arbitrary assignment of its element is illegal

        change_master_pw() # generate a new key using new master p/w

        conn = sqlite3.connect(db_path)
        for row in all_dec:  # re-encrypt the p/w column using new pw
            data_enc = master_key.encrypt(row[1])
            update_db(row[0], data_enc, "pw")
        conn.commit()

        os.remove(db_path+".old")

try:
    while True:
        # Read and validate domain
        url_read = input("Enter url to search record/ press <enter> to read from clipboard/ <q> to quit:\n")
        if url_read == "q": break
        if url_read == "": url_read = pyperclip.paste()
        url_extract = tldextract.extract(url_read)
        domain = url_extract.registered_domain
        if domain == "" or "." not in domain:
            print(f"Invalid URL detected: {domain}")
            continue

        # Create, retrieve or update password
        result = search_db(domain)
        if not result:
            new_entry(domain)
        else:
            update_retrieve(result)
except Exception as err:
    traceback.print_exc()

conn.close()