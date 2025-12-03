import sqlite3
from typing import Optional


# db_connection.py
import sqlite3

DB_PATH = "DATA/intelligence_platform.db"

def get_connection():
    """
    Create and return a new database connection.
    Usage:
        conn = get_connection()
        cursor = conn.cursor()
        ...
        conn.close()
    """
    return sqlite3.connect(DB_PATH)
