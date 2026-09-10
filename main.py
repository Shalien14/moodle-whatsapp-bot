from moodle.client import MoodleClient
from whatsapp.sender import send_message
from storage import load_seen_ids ,save_seen_ids


client = MoodleClient()
client.login()
notifications, unreadcount = client.get_notifications()

seen_ids = load_seen_ids()

print(seen_ids)

new_notifications = []

for notification in notifications[0:10]:
    if notification["id"] not in seen_ids:
        new_notifications.append(notification)

print("New notifications:", len(new_notifications))

for notification in new_notifications:
    print("--------------------")
    print("ID:", notification["id"])
    print("Subject:", notification["subject"])
    print("Content:", notification["smallmessage"])
    message = (
        "🔔 New Moodle Notification\n\n"
        f"📚 {notification['subject']}\n\n"
        f"{notification['smallmessage']}\n\n"
        f"🕒 {notification['timecreatedpretty']}\n"
        f"🔗 {notification['contexturl']}"
    )

    send_message(message)
    seen_ids.append(notification["id"])

print(seen_ids)
save_seen_ids(seen_ids)