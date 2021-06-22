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
# url_read = pyperclip.paste()
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

#######################################
### data for debug only ###
# def inserts_db(list_in):
#     conn = sqlite3.connect("pwmngr.db")
#     curs = conn.cursor()
#     curs.executemany("INSERT INTO pwtable VALUES (?,?)", list_in)
#     conn.commit()
#     conn.close()

# list1 = [
#         ("testing.com","abc0000^<"),
#         ("company.com", "iopqr013^"),
#         ("reg.org", "masl+_14m"),
#         ("services.com", "@jalgiu1"),
#         ("shopping.com", "LE%)@Ndkf"),
#         ("mall.com", "PamylqOQ1*"),
#         ("special.org", "aloJ71"),
#         ("greetings.com", "pqmmnpas/"),
# ]
# inserts_db(list1)
#######################################

# search for matching record -> new: / old:
url_read = "bad.com"
try:
    pw_read = search_db(url_read)
except:
    print("New web site detected.\n(1)Create new entry.\n(2)Search again.\n")
    pass
# print(type(pw_read))
# pyperclip.copy(pw_read)

# print("New web site detected.\n(1)Create new entry.\n(2)Search again.\n")
# print("Repeated record detected.\n(1)Retrieve password.\n(2)Update password.\n")