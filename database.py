import sqlite3

conn = sqlite3.connect('taskmanager.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
status TEXT,
user_id INTEGER
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")
