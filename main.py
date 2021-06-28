# Python program to manage login passwords

import pyperclip
import sqlite3

from pw_gen import pwgen
import tldextract
import argparse
from shutil import copy2
from pw_encrypt import key_read, master_pw, salt_gen, str_encrypt
from os import remove

from sys import platform
if platform.startswith("linux"):
    db_path = r"~/.database/pwmngr.db"
elif platform.startswith("win32"):
    db_path = r"d:\py_prjs\.database\pwmngr.db"
conn = sqlite3.connect(db_path)

parse = argparse.ArgumentParser()
parse.add_argument("--debug", action="store_true", help="Insert test data table to debug database.")
args = parse.parse_args()
#######################################
### data for debug only ###
if args.debug:
    conn.close()
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
        ("abc.com", "name@email.com", "", str_encrypt("pw_test1", key_read(), "en")),
        ("testing.com", "name@email.com", "hahaha", str_encrypt("pw_test2", key_read(), "en")),
        ("school.org", "myidno", "some notes", str_encrypt("pw_test3", key_read(), "en")),
    ]
    inserts_db(list1)
#######################################

def show_all():
    curs = conn.cursor()
    curs.execute("SELECT * FROM pwtable")
    data_row = curs.fetchall()
    print(*data_row,sep="\n")
    conn.commit()

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
        search_result = {"login":row[0], "re":row[1], "pw":str_encrypt(row[2], key_read(), "de")}
        return search_result

def update_db(url_in, data_in, opt):
    curs = conn.cursor()
    if opt == "pw":
        curs.execute("UPDATE pwtable SET password = (?) WHERE url = (?)", (data_in, url_in))
    elif opt == "log":
        curs.execute("UPDATE pwtable SET login = (?) WHERE url = (?)", (data_in, url_in))
    elif opt == "re":
        curs.execute("UPDATE pwtable SET remark = (?) WHERE url = (?)", (data_in, url_in))
    conn.commit()

def update_retrieve():
    user_opt = " "
    while user_opt != "1" and user_opt != "2" and user_opt != "3":
        print(f"Record found. Login ID: {s_result['login']}  (Note: {s_result['re']}).")
        user_opt = input("(1)Retrieve password. (2)Generate new password & update the record. (3)Update database Login ID and note.==> ")
        if user_opt == "1":
            pyperclip.copy(s_result["pw"])
            print("Password copied to clipboard!")
        elif user_opt == "2":
            new_pw = pwgen()
            new_pw_enc = str_encrypt(new_pw, key_read(), "en")
            update_db(domain, new_pw_enc, "pw")
            pyperclip.copy(new_pw)
            print(f"Password for {domain} (Note: {s_result['re']}) updated and copied to clipboard!\nLogin & Password are: {s_result['login']}:|  {new_pw}  |")
        elif user_opt == "3":
            update_input = input("Input new Login ID and note (separated by ';'): ")
            if update_input != "":
                update_in = update_input.split(";", 1)
                update_db(domain, update_in[0].strip(), "log")
                if update_in[1]: update_db(domain, update_in[1].strip(), "re")
                print(f"Database updated for {domain} (Note: {search_db(domain)['re']}), Login ID: {search_db(domain)['login']}")
        else:
            print("Error, please enter 1, 2 or 3.")

def delete_db():
    # add code here
    return


print("***Python Password Manager***")

curs = conn.cursor()
curs.execute("SELECT count(name) FROM sqlite_master WHERE type= 'table' AND name='pwtable' ")
if curs.fetchone()[0]==1:       # if pwtable exist -> use master to login
    conn.commit()
    master_pw("login")
    if input("Press <enter> to continue, or <Ch> to change master password: ") == "Ch":
        copy2(db_path, db_path+".old")
        conn.close()
        
        conn = sqlite3.connect(db_path+".old")
        curs = conn.cursor()
        curs.execute("SELECT url, password FROM pwtable")
        all_rows = curs.fetchall()
        conn.commit()
        all_dec = []
        for i in all_rows:  # decrypt using existing key
            data_de = str_encrypt(i[1], key_read(), "de")
            all_dec += [(i[0], data_de)]     # i is a tuple, arbitrary assignment of its element is illegal
        del all_rows
        master_pw("change") # generate a new key using new master p/w
        conn.close()
        
        conn = sqlite3.connect(db_path)
        for i in all_dec:  # re-encrypt the p/w column using new m_pw
            data_en = str_encrypt(i[1], key_read(), "en")
            i = (i[0], data_en)
            update_db(i[0], i[1], "pw")
        del all_dec
        conn.commit()
        # master_pw("del_old")    # delete the key.old
        # remove(db_path+".old")
else:               # if no, create a salt then master password and store the key
    salt_gen()
    master_pw("new")
    
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

try:
    while True:
        url_read = input("Enter url to search record/ press <enter> to read from clipboard/ <q> to quit:\n")
        if url_read == "q": break
        if url_read == "": url_read = pyperclip.paste()
        url_extract = tldextract.extract(url_read)
        domain = url_extract.registered_domain
        if domain == "" or "." not in domain:
            print(f"Invalid URL detected: {domain}")
            continue
        s_result = search_db(domain)
        if not s_result: # new and create entry
            user_opt = input(f"New web site detected: {domain}\n(1)Create new entry,\n(Otherwise)Search again.\n")
            if user_opt == "1":
                new_login = input(f"Login id/email for {domain}: ")
                new_remark = input(f"Additional note: ")
                new_pw = pwgen()
                pyperclip.copy(new_pw)
                new_pw_enc = str_encrypt(new_pw, key_read(), "en")
                insert_db(domain, new_login, new_remark, new_pw_enc)
                print(f"New entry created for {domain}\nLogin & Password are: {new_login}:|  {new_pw}  | Password copied to clipboard!")
            else: continue
        else: # old record found
            update_retrieve() # update or retrieve
except Exception as err:
    print("Exception: ", err)

conn.close()