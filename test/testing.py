import sqlite3

conn = sqlite3.connect("../test.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM operation_log")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
