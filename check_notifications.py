import json
from moodle.client import MoodleClient
from whatsapp.sender import send_message
client = MoodleClient()
client.login()
notifications, unreadcount = client.get_notifications()

with open("data/seen_notifications.json", "r") as file:
    seen_ids = json.load(file)

print(seen_ids)

new_notifications = []

for notification in notifications[0:7]:
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
with open("data/seen_notifications.json", "w") as file:
    json.dump(seen_ids, file)