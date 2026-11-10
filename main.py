
import os
import time

from dotenv import load_dotenv

from moodle.client import MoodleClient
from moodle.formatter import format_notification
from whatsapp.sender import send_template
from storage import load_seen_ids, save_seen_ids

load_dotenv()

CHECK_INTERVAL = 600
RETRY_INTERVAL = 60

TEMPLATE_NAME = os.getenv("WHATSAPP_TEMPLATE_NAME")
TEMPLATE_LANGUAGE = os.getenv("WHATSAPP_TEMPLATE_LANGUAGE", "en")


def check_notifications(client):
    notifications, unread_count = client.get_notifications()

    seen_ids = set(load_seen_ids())

    new_notifications = [
        notification
        for notification in notifications[::-1]
        if notification["id"] not in seen_ids
    ]

    print("Total notifications:", len(notifications))
    print("Unread notifications:", unread_count)
    print("New notifications:", len(new_notifications))

    for notification in new_notifications:
        notification_id = notification["id"]

        try:
            parameters = format_notification(notification)

            print("--------------------")
            print("ID:", notification_id)
            print("Subject:", notification["subject"])
            print("Course:", parameters[0])

            result = send_template(
                TEMPLATE_NAME,
                TEMPLATE_LANGUAGE,
                parameters,
            )

            # Record only after successful API acceptance.
            seen_ids.add(notification_id)
            save_seen_ids(list(seen_ids))

            print("WhatsApp API accepted:", result.get("messages", []))

        except Exception as error:
            print(
                f"Failed to process notification {notification_id}:",
                error,
            )


def main():
    if not TEMPLATE_NAME:
        raise ValueError("WHATSAPP_TEMPLATE_NAME is missing from .env")

    client = MoodleClient()

    print("Starting UoM Moodle WhatsApp bot")

    try:
        while True:
            try:
                print("\nConnecting to Moodle...")
                client.login()

                check_notifications(client)

                print(f"Waiting {CHECK_INTERVAL // 60} minutes...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                print("\nStopping Moodle bot...")
                break

            except Exception as error:
                print("Moodle check failed:", error)
                print(f"Retrying in {RETRY_INTERVAL} seconds...")

                time.sleep(RETRY_INTERVAL)

    finally:
        client.session.close()
        print("Moodle bot stopped.")


if __name__ == "__main__":
    main()
