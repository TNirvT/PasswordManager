# Python program to manage login passwords

import pyperclip
import sqlite3
from pw_gen import *

def search_db(url_in):
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM pwtable WHERE url = (?)", (url_in,))
    row = curs.fetchone()
    conn.commit()
    conn.close()
    return row[1]

def update_db():
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    conn.commit()
    conn.close()
    return

def insert_db(url_in, pw_in):
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO pwtable VALUES (?,?)", (url_in, pw_in))
    conn.commit()
    conn.close()

###############################

print("***Python Password Manager***")
url_read = pyperclip.paste()

try:
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("""
        CREATE TABLE pwtable (
            url text,
            password text
        )
    """)
    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    pass

# search for matching record -> new: / old:
pw_read = search_db(url_read)
pyperclip.copy(pw_read)

# print("New web site detected.\n(1)Create new entry.\n(2)Search again.\n")
# print("Repeated record detected.\n(1)Retrieve password.\n(2)Update password.\n")