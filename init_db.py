import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (tName, tDescription, endDate) VALUES (?, ?, ?)",
            ('First task', 'tDescription for the first task', '2023/08/30'))

cur.execute("INSERT INTO tasks (tName, tDescription, endDate) VALUES (?, ?, ?)",
            ('Second task', 'tDescription for the second task', '2023/08/30'))

connection.commit()
connection.close()