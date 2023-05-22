import sqlite3

def insert_user(realname, username, password):
    conn = sqlite3.connect("users.db")
    print("Accessing Database")
    print("Adding User to Database")
    conn.execute(f"INSERT INTO USERS (REALNAME,USERNAME,PASSWORD) \
                 VALUES ('{realname}','{username}','{password}')")
    conn.commit()
    print(f"{username} added")
    conn.close()

accounts =[["Max","Max66","Goodbye"],["James","James123","IDK"],["Jamie","Jamie!!!!","Jamie!!"],["Mathew","BigDog6","Hek12"],["Josh","JoshtheHippo","ILoveHippos"]]

print("Staring Task")
for account in accounts:
    insert_user(account[0],account[1],account[2])
    print("adding",account[1])
print("All users added")
