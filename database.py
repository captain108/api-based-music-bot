import sqlite3

conn = sqlite3.connect("music.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS playlists (
    chat_id INTEGER,
    name TEXT,
    url TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    chat_id INTEGER PRIMARY KEY,
    volume INTEGER DEFAULT 100,
    loop INTEGER DEFAULT 0
)
""")

conn.commit()


def add_playlist(chat_id, name, url):
    cursor.execute("INSERT INTO playlists VALUES (?, ?, ?)", (chat_id, name, url))
    conn.commit()


def get_playlist(chat_id):
    cursor.execute("SELECT name, url FROM playlists WHERE chat_id=?", (chat_id,))
    return cursor.fetchall()
