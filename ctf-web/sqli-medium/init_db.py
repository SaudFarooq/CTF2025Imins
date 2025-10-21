import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, is_admin INTEGER DEFAULT 0)')
c.execute('DELETE FROM users')
c.execute('INSERT INTO users (username, password, is_admin) VALUES ("guest", "guest", 0)')
c.execute('INSERT INTO users (username, password, is_admin) VALUES ("admin", "supersecret", 1)')
conn.commit()
conn.close()
