"""
Script for inspecting SQLite database tables.

Connects to the `info.db` SQLite database, retrieves all rows
from the `operation_log` and `users` tables and prints
the results to the console.
"""

import sqlite3

conn = sqlite3.connect("../info.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM operation_log")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
