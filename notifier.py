import os
import requests


def send_discord_alert(monitor_id, deadline):

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError("Discord webhook URL not configured")

    message = {
        "content": (
            f"HEARTBEAT ALERT!\n"
            f"Monitor {monitor_id} missed its deadline!\n"
            f"Deadline: {deadline}"
        ),
        "allowed_mentions": {"parse": []}
    }

    response = requests.post(
        webhook_url,
        json=message,
        params={"wait": "true"},
        timeout=10
    )

    response.raise_for_status()

    return True