# Python program to manage login passwords

from sys import path
import pyperclip
import sqlite3
from pw_gen import pwgen
import tldextract
import argparse

print("***Python Password Manager***")
db_path = r"d:\py_prjs\database\pwmngr.db"
conn = sqlite3.connect(db_path)

parse = argparse.ArgumentParser()
parse.add_argument("--setup", action="store_true", help="Create table in database.")
parse.add_argument("--debug", action="store_true", help="Insert test data table to debug database.")
args = parse.parse_args()
#######################################
### data for debug only ###
if args.debug:
    conn.close()
    conn = sqlite3.connect("pwmngr_debug.db")
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS pwtable (
        url text,
        password text
        )
    """)
    def inserts_db(list_in):
        curs = conn.cursor()
        curs.executemany("INSERT INTO pwtable VALUES (?,?)", list_in)
        conn.commit()

    list1 = [
        ("testing.com","abc0000^<"),
        ("company.com", "iopqr013^"),
        ("reg.org", "masl+_14m"),
        ("services.com", "@jalgiu1"),
        ("shopping.com", "LE%)@Ndkf"),
        ("mall.com", "PamylqOQ1*"),
        ("special.org", "aloJ71"),
        ("greetings.com", "pqmmnpas/"),
    ]
    inserts_db(list1)
#######################################

def show_all():
    curs = conn.cursor()
    curs.execute("SELECT * FROM pwtable")
    data_row = curs.fetchall()
    print(*data_row,sep="\n")
    conn.commit()

def search_db(url_in):
    curs = conn.cursor()
    curs.execute("SELECT password FROM pwtable WHERE url = (?)", (url_in,))
    row = curs.fetchone()
    conn.commit()
    if not row:
        return None
    else:
        return row[0]

def update_db(url_in, pw_in):
    curs = conn.cursor()
    curs.execute("UPDATE pwtable SET password = (?) WHERE url = (?)", (pw_in, url_in))
    conn.commit()

def update_retrieve():
    user_opt = " "
    while user_opt != "1" and user_opt != "2":
        user_opt = input("Existing reecord found.\n(1)Retrieve password.\n(2)Update password.\n")
        if user_opt == "1":
            pyperclip.copy(s_result)
            print("Password copied to clipboard!")
        elif user_opt == "2":
            new_pw = pwgen()
            update_db(url_read, new_pw)
            pyperclip.copy(new_pw)
            print(f"Password for {url_read} updated and copied to clipboard!\nPassword:||  {new_pw}  ||")
        else:
            print("Error, please enter 1 or 2.")

def delete_db():
    # add code here
    return

def insert_db(url_in, pw_in):
    curs = conn.cursor()
    curs.execute("INSERT INTO pwtable VALUES (?,?)", (url_in, pw_in))
    conn.commit()

if args.setup:
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS pwtable (
        url text,
        password text
        )
    """)
    conn.commit()

while True:
    try:
        url_read = input("Enter url to search record/ press <enter> to read from clipboard:\n")
        if url_read == "": url_read = pyperclip.paste()
        url_extract = tldextract.extract(url_read)
        url_read = url_extract.registered_domain
        s_result = search_db(url_read)
        if not s_result and url_read != "" and "." in url_read: # new and create entry
            user_opt = input(f"New web site detected: {url_read}\n(1)Create new entry, or <q> to quit.\n(Otherwise)Search again.\n")
            if user_opt == "1":
                new_pw = pwgen()
                insert_db(url_read,new_pw)
                print(f"New entry created for {url_read}\nPassword:||  {new_pw}  ||")
                break
            elif user_opt == "Q" or user_opt == "q":
                break
        elif url_read == "" or "." not  in url_read:
            print(f"Invalid URL detected: {url_read}")
            pass
        else: # old record found
            update_retrieve() # update or retrieve
            break 
    except Exception as err:
        print("Exception: ", err)

conn.close()