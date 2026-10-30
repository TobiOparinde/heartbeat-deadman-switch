import sqlite3
from datetime import datetime, timedelta, timezone

DB_PATH = "heartbeat.db"


def create_table():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS monitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interval_seconds INTEGER NOT NULL,
            deadline TEXT NOT NULL
        )
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_id INTEGER NOT NULL,
        deadline TEXT NOT NULL,
        UNIQUE(monitor_id, deadline)
        )
    """)

    connection.commit()
    connection.close()

def save_monitor(interval_seconds):

    now = datetime.now(timezone.utc)
    deadline = now + timedelta(seconds=interval_seconds)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute(
        "INSERT INTO monitors (interval_seconds, deadline) VALUES (?, ?)",
        (interval_seconds, deadline.isoformat())
    )

    connection.commit()

    monitor_id = cursor.lastrowid
    connection.close()

    return monitor_id, deadline

def get_monitors():

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    monitors = connection.execute("SELECT * FROM monitors")
    monitors = monitors.fetchall()

    monitors = [dict(row) for row in monitors]

    connection.close()

    return monitors

def check_in(monitor_id):

    connection = sqlite3.connect(DB_PATH)

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

    now = datetime.now(timezone.utc).isoformat()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "SELECT * FROM monitors WHERE deadline <= ?",
        (now,)
    )

    overdue = cursor.fetchall()
    connection.close()

    return [dict(row) for row in overdue]

def record_alert(monitor_id, deadline):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO alerts (monitor_id, deadline)
        VALUES (?, ?)
        """,
        (monitor_id, deadline)
    )

    connection.commit()

    was_inserted = cursor.rowcount == 1

    connection.close()

    return was_inserted




    