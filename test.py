import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")

conn.execute('''CREATE TABLE USERS
             (REALNAME            TEXT NOT NULL,
              USERNAME            TEXT NOT NULL,
              PASSWORD            TEXT NOT NULL);''')

print("Table created successfully")

#conn.commit()
conn.close()