import sqlite3
from datetime import datetime, timedelta, timezone
import database


def test_check_in_resets_deadline(tmp_path, monkeypatch):

    monkeypatch.setattr(
        database,
        "DB_PATH",
        str(tmp_path / "test.db")
    )

    database.create_table()

    # Create a monitor
    monitor_id, deadline = database.save_monitor(60)

    # Simulate an expired deadline
    expired = datetime.now(timezone.utc) - timedelta(minutes=5)

    connection = sqlite3.connect(database.DB_PATH)
    connection.execute(
        "UPDATE monitors SET deadline = ? WHERE id = ?",
        (expired.isoformat(), monitor_id)
    )
    connection.commit()
    connection.close()

    # Verify the monitor is overdue
    overdue = database.get_overdue_monitors()
    assert any(m["id"] == monitor_id for m in overdue)

    # Check in and reset the deadline
    new_deadline = database.check_in(monitor_id)

    assert new_deadline > datetime.now(timezone.utc)

    # Verify the monitor is no longer overdue
    overdue = database.get_overdue_monitors()
    assert not any(m["id"] == monitor_id for m in overdue)

def test_invalid_monitor_id(tmp_path, monkeypatch):

    monkeypatch.setattr(
        database,
        "DB_PATH",
        str(tmp_path / "test.db")
    )

    database.create_table()

    result = database.check_in(999999)

    assert result is None