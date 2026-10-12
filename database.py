import sqlite3
from datetime import datetime, timedelta, timezone


def create_table():
    connection = sqlite3.connect("heartbeat.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS monitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interval_seconds INTEGER NOT NULL,
            deadline TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def save_monitor(interval_seconds):

    now = datetime.now(timezone.utc)
    deadline = now + timedelta(seconds=interval_seconds)

    connection = sqlite3.connect("heartbeat.db")

    cursor = connection.execute(
        "INSERT INTO monitors (interval_seconds, deadline) VALUES (?, ?)",
        (interval_seconds, deadline.isoformat())
    )

    connection.commit()

    monitor_id = cursor.lastrowid
    connection.close()

    return monitor_id, deadline