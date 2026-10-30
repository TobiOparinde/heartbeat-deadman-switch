import database

def test_duplicate_alerts_are_ignored(tmp_path, monkeypatch):

    monkeypatch.setattr(
        database,
        "DB_PATH",
        str(tmp_path / "test.db")
    )

    database.create_table()

    # Create a real monitor in our test database
    monitor_id, deadline = database.save_monitor(60)
    deadline = deadline.isoformat()

    # First alert should succeed
    assert database.record_alert(monitor_id, deadline) == True

    # Duplicate alert should be ignored
    assert database.record_alert(monitor_id, deadline) == False