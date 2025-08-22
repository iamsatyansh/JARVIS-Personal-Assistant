# ==============================================================================
# File: core/database.py
# ==============================================================================
class DatabaseManager:
    """Manages SQLite database operations."""
    def __init__(self, db_path: str):
        from pathlib import Path
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Note: For a truly async app, a library like aiosqlite would be ideal.
        # Here, we use run_in_executor to handle blocking calls.
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._setup_tables()

    def _setup_tables(self):
        # This is a blocking call, but it's only done once at startup.
        cursor = self.conn.cursor()
        # CRITICAL FIX: Create the 'memories' table before the virtual FTS table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT
            );
        """)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content, category, tags, content='memories', content_rowid='id'
            );
        """)
        self.conn.commit()

    async def _execute_in_executor(self, func, *args):
        """Runs a blocking database function in a thread pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)

    def _store_memory_blocking(self, content: str, category: str, tags: list):
        # This is the blocking function to be run in an executor
        tags_json = json.dumps(tags or [])
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO memories (content, category, tags) VALUES (?, ?, ?)",
                       (content, category, tags_json))
        self.conn.commit()

    async def store_memory(self, content: str, category: str, tags: list):
        await self._execute_in_executor(self._store_memory_blocking, content, category, tags)

    def _recall_memories_blocking(self, query: str):
        cursor = self.conn.cursor()
        # Simple search for demonstration; FTS would be better
        cursor.execute("SELECT * FROM memories WHERE content LIKE ?", (f'%{query}%',))
        return cursor.fetchall()

    async def recall_memories(self, query: str):
        return await self._execute_in_executor(self._recall_memories_blocking, query)

    async def close(self):
        await self._execute_in_executor(self.conn.close)
        logging.info("Database connection closed.")
