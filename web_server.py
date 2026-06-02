from flask import Flask, request
from resources import Entry
from EntryManager import EntryManager
import os

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Конфигурация БД (берётся из env, если нет — используются значения по умолчанию)
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "todolist"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "secret"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

db_manager = EntryManager(DB_CONFIG)
db_manager.init_db()

@app.route("/api/entries/")
def get_entries():
    db_manager.load()

    return [entry.json() for entry in db_manager.entries]

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    data = request.get_json()

    for item in data:
        entry = Entry.entry_from_json(item)
        db_manager.entries.append(entry)
    db_manager.save()

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

