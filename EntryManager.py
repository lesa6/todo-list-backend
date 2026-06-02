from resources import Entry
from typing import List
import psycopg2
import psycopg2.extras

class EntryManager:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self._conn = None
        self.entries: List[Entry] = []
    
    def init_db(self):
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                );
            """)
            conn.commit()
    
    def _get_conn(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(**self.db_config)
        return self._conn
    
    def save(self):
        for entry in self.entries:
            entry.save(self._get_conn())

    def load(self):
        conn = self._get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT data FROM entries;")
            rows = cur.fetchall()
            
            self.entries = []
            for row in rows:
                if row['data']:
                    content = Entry.load(row['data'])
                    if content:
                        self.entries.append(content)
        return []


    def add_entry(self, title:str):
        entry = Entry(title)
        self.entries.append(entry)

