import sqlite3

connection = sqlite3.connect("sqlite.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE  IF NOT EXISTS shipment (
        id INTEGER,
        content TEXT,
        weight REAL,
        status TEXT
    );
""")

connection.close()

