import time
import requests

from database import get_overdue_monitors, record_alert
from notifier import send_discord_alert


def run_worker():

    while True:
        overdue_list = get_overdue_monitors()

        for monitor in overdue_list:

            inserted = record_alert(
                monitor["id"],
                monitor["deadline"]
            )

            if inserted:
                try:
                    send_discord_alert(
                        monitor["id"],
                        monitor["deadline"]
                    )

                    print("Notification sent:", monitor["id"])

                except (requests.RequestException, RuntimeError) as error:
                    print(
                        "Notification failed:",
                        monitor["id"],
                        type(error).__name__
                    )

        time.sleep(5)


if __name__ == "__main__":
    run_worker()