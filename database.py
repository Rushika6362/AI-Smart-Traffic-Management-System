import sqlite3

conn = sqlite3.connect("traffic.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic(
id INTEGER PRIMARY KEY,
count INTEGER,
status TEXT,
green_time INTEGER
)
""")

conn.commit()
conn.close()