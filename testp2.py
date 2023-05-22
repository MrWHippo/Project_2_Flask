import sqlite3

conn = sqlite3.connect("test.db")
print("Opened database succesfully")

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)  \
             VALUES (1, 'Paul', 32, 'California', 20000.00)");

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)  \
             VALUES (2, 'James', 19, 'UTAH', 1200000.00)");

conn.commit()
print("Records created successfully")
conn.close()