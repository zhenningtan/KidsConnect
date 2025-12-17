import sqlite3
import hashlib
import os
import json

DB_NAME = "kids_activity.db"

def init_db():
    """Initialize the database with users and completions tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')

    # Completions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            username TEXT,
            date TEXT,
            PRIMARY KEY (username, date),
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    # Activity Overrides table
    # Stores the specific activity assigned to a user for a specific date
    # This handles the "Random" activity feature
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_overrides (
            username TEXT,
            date TEXT,
            activity_data TEXT, -- JSON string of the activity
            PRIMARY KEY (username, date),
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user. Returns True if successful, False if username exists."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    pwd_hash = hash_password(password)

    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, pwd_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Verify user credentials. Returns True if valid."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    pwd_hash = hash_password(password)

    c.execute('SELECT 1 FROM users WHERE username = ? AND password_hash = ?', (username, pwd_hash))
    user = c.fetchone()
    conn.close()

    return user is not None

def get_user_completions(username):
    """Return a set of completed dates for the user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT date FROM completions WHERE username = ?', (username,))
    dates = {row[0] for row in c.fetchall()}
    conn.close()
    return dates

def toggle_completion(username, date_str):
    """Toggle completion status for a user and date. Returns the new status (True/False)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT 1 FROM completions WHERE username = ? AND date = ?', (username, date_str))
    exists = c.fetchone()

    if exists:
        c.execute('DELETE FROM completions WHERE username = ? AND date = ?', (username, date_str))
        is_completed = False
    else:
        c.execute('INSERT INTO completions (username, date) VALUES (?, ?)', (username, date_str))
        is_completed = True

    conn.commit()
    conn.close()
    return is_completed

def save_activity_override(username, date_str, activity_data):
    """Save a specific activity for a user on a date (overriding the default)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    activity_json = json.dumps(activity_data)

    c.execute('''
        INSERT OR REPLACE INTO activity_overrides (username, date, activity_data)
        VALUES (?, ?, ?)
    ''', (username, date_str, activity_json))

    conn.commit()
    conn.close()

def get_activity_override(username, date_str):
    """Get the overridden activity for a user on a date, if any."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('SELECT activity_data FROM activity_overrides WHERE username = ? AND date = ?', (username, date_str))
    row = c.fetchone()
    conn.close()

    if row:
        return json.loads(row[0])
    return None
