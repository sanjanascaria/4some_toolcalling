import sqlite3

DB_PATH = "4some_db.db"
CSV_PATH = "4some_users.csv"

def get_conn():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            personality_type TEXT,
            age_range TEXT,
            interest TEXT,
            location TEXT,
            willing_to_travel TEXT,
            gender_pref TEXT,
            feedback TEXT DEFAULT ''
        );
        """)
        conn.commit()