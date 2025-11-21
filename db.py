import sqlite3
from typing import Optional

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
conn = sqlite3.connect("DATA\\intelligence_platform.db")


class DatabaseLayer:
    def __init__(self, db_path: str, timeout: int = 5) -> None:
        """Initialize with database path and optional timeout."""
        self.db_path = db_path
        self.timeout = timeout
        self.conn: Optional[sqlite3.Connection] = None

    def _row_factory(self, cursor, row):
        """Convert rows to dicts for easier access."""
        return {cursor.description[i][0]: row[i] for i in range(len(row))}

    def connect(self) -> None:
        """Open a SQLite connection and configure row factory."""
        if self.conn:
            return
        self.conn = sqlite3.connect(self.db_path, timeout=self.timeout)
        self.conn.row_factory = self._row_factory

    def close(self) -> None:
        """Close the connection if open."""
        if self.conn:
            try:
                self.conn.commit()
            finally:
                self.conn.close()
                self.conn = None

    def __enter__(self) -> "DatabaseLayer":
        """Context manager entry: open connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Context manager exit: rollback on error, close connection."""
        if exc_type and self.conn:
            self.conn.rollback()
        self.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query without returning results (INSERT/UPDATE/DELETE)."""
        if not self.conn:
            self.connect()
        self.conn.execute(query, params)

    def fetchall(self, query: str, params: tuple = ()) -> list[dict]:
        """Execute a SELECT and return all rows as dicts."""
        if not self.conn:
            self.connect()
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Execute a SELECT and return a single row as dict."""
        if not self.conn:
            self.connect()
        cursor = self.conn.execute(query, params)
        return cursor.fetchone()