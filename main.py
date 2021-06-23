# Python program to manage login passwords

import pyperclip
import sqlite3
from pw_gen import *

def show_all():
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM pwtable")
    data_row = curs.fetchall()
    print(*data_row,sep="\n")
    conn.commit()
    conn.close()

def search_db(url_in):
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM pwtable WHERE url = (?)", (url_in,))
    row = curs.fetchone()
    conn.commit()
    conn.close()
    if type(row) is not tuple:
        return "NULL"
    else:
        return row[1]

def update_db(url_in, pw_in):
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("UPDATE pwtable SET password = (?) WHERE url = (?)", (pw_in, url_in))
    conn.commit()
    conn.close()

def update_retrieve(url_in):
    pw_read = search_db(url_in)
    user_opt = " "
    while user_opt != "1" and user_opt != "2":
        user_opt = input("Repeated record detected.\n(1)Retrieve password.\n(2)Update password.\n")
        if user_opt == "1":
            pyperclip.copy(pw_read)
            print("Password copied to clipboard!")
        elif user_opt == "2":
            new_pw = genpw()
            update_db(url_read, new_pw)
            pyperclip.copy(new_pw)
            print(f"Password for {url_read} updated and copied to clipboard!\nPassword:||  {new_pw}  ||")
        else:
            print("Error, please enter 1 or 2.")

def delete_db():
    # add code here
    return

def insert_db(url_in, pw_in):
    conn = sqlite3.connect("pwmngr.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO pwtable VALUES (?,?)", (url_in, pw_in))
    conn.commit()
    conn.close()


print("***Python Password Manager***")

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

while True:
    try:
        url_read = pyperclip.paste()    # search for record
        ######################
        url_read = "badtesting.com" # for debug ONLY!!!!
        ######################
        s_result = search_db(url_read)
        if s_result == "NULL": # new and create entry
            user_opt = input("New web site detected.\n(1)Create new entry.\n(Otherwise)Search again.\n")
            if user_opt == "1":
                new_pw = genpw()
                insert_db(url_read,new_pw)
                print(f"New entry created for {url_read}\nPassword:||  {new_pw}  ||")
                break
        else: # old record found
            update_retrieve(url_read) # update or retrieve
            break 
    except:
        pass
