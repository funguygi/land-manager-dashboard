import sqlite3

DB_NAME = "grants.db"


def set_last_refresh(timestamp):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.execute("""
    INSERT OR REPLACE INTO metadata
    (key, value)
    VALUES (?, ?)
    """, (
        "last_refresh",
        timestamp
    ))

    conn.commit()
    conn.close()


def get_last_refresh():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    row = conn.execute("""
    SELECT value
    FROM metadata
    WHERE key='last_refresh'
    """).fetchone()

    conn.close()

    if row:
        return row[0]

    return "Never"