import sqlite3
from datetime import datetime


# working - is_a_user
def test_1():
    username = "bobb"

    conn = sqlite3.connect("userdata.db")

    cur = conn.cursor()
    cur.execute(f"SELECT username FROM users WHERE username = '{username}'")

    length = len(cur.fetchall())

    print(length)
    #value = (cur.fetchall())[0][0]
    #print(value)
    

#working - insert_new_user
def test_2():
    
    conn = sqlite3.connect("userdata.db")
    now = datetime.now()
    #cur = conn.cursor()
    conn.execute(f"INSERT INTO users (username, password, real_name, city, last_login, account_creation_date) VALUES ('bob','bob','bob','oxford','{now}','{now}');")

    conn.commit()

#working - update login time
def test_3():
    
    username = 'bob'
    conn = sqlite3.connect("userdata.db")
    now = datetime.now()

    conn.execute(f"UPDATE users SET last_login = '{now}' WHERE username = '{username}'")

    conn.commit()

def valid_password(password):
    listpassword = list(password)
    for character in listpassword:
        if character == "\"" or character == "\\" or character == " ":
            return False
    return True

def test_4():
    conn = sqlite3.connect("userdata.db")

    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")

    value = cur.fetchall()
    return value

#test_3()
#print(valid_password("88"))
print(test_4())

