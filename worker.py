import time
from database import get_overdue_monitors, record_alert


def run_worker():

    while True:

        overdue_list = get_overdue_monitors()

        for monitor in overdue_list:

            inserted = record_alert(
                monitor["id"],
                monitor["deadline"]
            )

            if inserted:
                print(
                    "ALERT:",
                    monitor["id"],
                    monitor["deadline"]
                )

        time.sleep(5)


if __name__ == "__main__":
    run_worker()