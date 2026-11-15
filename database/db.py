
import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "MAFDES.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                input_facts TEXT,
                diagnoses TEXT
            )
        """)


def save_diagnosis(result):

    with get_connection() as connection:

        connection.execute("""
            INSERT INTO diagnosis_history
            (timestamp, input_facts, diagnoses)
            VALUES (?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            json.dumps(result.get("input_facts", [])),
            json.dumps(result.get("diagnoses", []))
        ))


def get_diagnosis_history():

    with get_connection() as connection:

        records = connection.execute("""
            SELECT id, timestamp, input_facts, diagnoses
            FROM diagnosis_history
            ORDER BY id DESC
        """).fetchall()

    return [
        {
            "id": row[0],
            "timestamp": row[1],
            "input_facts": json.loads(row[2]),
            "diagnoses": json.loads(row[3])
        }
        for row in records
    ]