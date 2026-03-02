import sqlite3

conn = sqlite3.connect("music.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    chat_id INTEGER PRIMARY KEY,
    volume INTEGER DEFAULT 100,
    loop INTEGER DEFAULT 0
)
""")

conn.commit()

def get_settings(chat_id):
    cursor.execute("SELECT volume, loop FROM settings WHERE chat_id=?", (chat_id,))
    row = cursor.fetchone()
    if row:
        return row
    cursor.execute("INSERT INTO settings (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    return (100, 0)
