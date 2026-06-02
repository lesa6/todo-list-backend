import json
import uuid
import psycopg2
import psycopg2.extras
from typing import Self

def print_with_indent(value, indent=0):
    indentation = " " * indent
    print(indentation + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None, entry_id=None):
        if entries is None:
            entries = []
        self.id = entry_id or str(uuid.uuid4())
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {"id": self.id, "title": self.title, "entries": [entry.json() for entry in self.entries]}
        return res
    
    @classmethod
    def entry_from_json(cls, value: dict) -> Self:
        new_entry = cls(value['title'], entry_id=value.get('id'))
        for item in value.get('entries', []):
            new_entry.add_entry(cls.entry_from_json(item))
        return new_entry
    
    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def save(self, conn):
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO entries (id, data) 
                VALUES (%s, %s)
                ON CONFLICT (id) 
                DO UPDATE SET data = EXCLUDED.data;
                """, (self.id, json.dumps(self.json())))
            conn.commit()

    @classmethod
    def load(cls, data):
        if data:  # Проверяем на None и пустую строку
            return cls.entry_from_json(json.loads(data))
        return None
    

    