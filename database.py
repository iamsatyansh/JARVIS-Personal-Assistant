# ==============================================================================
# File: database.py
# Description: Manages all SQLite database operations for JARVIS, including
#              preferences and memories.
# ==============================================================================
import sqlite3
import logging
import json
from datetime import datetime
from typing import List, Any

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handles all database operations for JARVIS."""

    def __init__(self, db_path: str = "jarvis_memory.db"):
        self.db_path = db_path
        self.conn = None
        try:
            # The check_same_thread=False is important for use with asyncio/threading
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.setup_tables()
        except sqlite3.Error as e:
            logger.critical(f"Database connection failed: {e}", exc_info=True)
            raise

    def setup_tables(self):
        """Creates necessary tables if they do not exist."""
        try:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL
                    )
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                """)
        except sqlite3.Error as e:
            logger.error(f"Failed to set up database tables: {e}")

    def store_memory(self, content: str):
        """Stores a memory snippet."""
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO memories (content, timestamp) VALUES (?, ?)",
                    (content, datetime.now().isoformat())
                )
        except sqlite3.Error as e:
            logger.error(f"Failed to store memory: {e}")

    def recall_memories(self, query: str) -> List[str]:
        """Recalls memories matching a query."""
        try:
            with self.conn:
                cursor = self.conn.execute(
                    "SELECT content FROM memories WHERE content LIKE ? ORDER BY timestamp DESC LIMIT 5",
                    (f"%{query}%",)
                )
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Failed to recall memories for query '{query}': {e}")
            return []

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
