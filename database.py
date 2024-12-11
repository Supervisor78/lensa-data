import sqlite3
from logic.config import DB_PATH

def get_connection():
    # Returnează conexiunea la baza de date SQLite
    return sqlite3.connect(DB_PATH)
