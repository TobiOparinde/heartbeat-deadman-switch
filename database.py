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

def get_monitors():

    connection = sqlite3.connect("heartbeat.db")
    connection.row_factory = sqlite3.Row

    monitors = connection.execute("SELECT * FROM monitors")
    monitors = monitors.fetchall()

    monitors = [dict(row) for row in monitors]

    connection.close()

    return monitors

def check_in(monitor_id):

    connection = sqlite3.connect("heartbeat.db")

    cursor = connection.execute(
        "SELECT interval_seconds FROM monitors WHERE id = ?",
        (monitor_id,)
    )

    monitor = cursor.fetchone()

    if monitor is None:
        connection.close()
        return None

    interval_seconds = monitor[0]

    now = datetime.now(timezone.utc)
    new_deadline = now + timedelta(seconds=interval_seconds)

    connection.execute(
        "UPDATE monitors SET deadline = ? WHERE id = ?",
        (new_deadline.isoformat(), monitor_id)
    )

    connection.commit()
    connection.close()

    return new_deadline

def get_overdue_monitors():
    now = datetime.now(timezone.utc).isofformat()

def get_overdue_monitors():

    now = datetime.now(timezone.utc).isoformat()

    connection = sqlite3.connect("heartbeat.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "SELECT * FROM monitors WHERE deadline <= ?",
        (now,)
    )

    overdue = cursor.fetchall()
    connection.close()

    return [dict(row) for row in overdue]




    