import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")

test = 2

if test == 1:
    cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
    for row in cursor:
       print("ID = ", row[0])
       print("NAME = ", row[1])
       print("ADDRESS = ", row[2])
       print("SALARY = ", row[3], "\n")

elif test == 2:
    conn = sqlite3.connect("test.db")
    print("Accessing Database.")
    name = 'Paul'
    userinfo = conn.execute(f"SELECT id, name, address, salary from COMPANY where name='{name}'")
    for value in userinfo:
        conn.close()
        print("user found")
        exit()
    conn.close()
    print("No user")
    

print ("Operation done successfully")
conn.close()