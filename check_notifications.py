import json
from moodle.client import MoodleClient

client = MoodleClient()
client.login()
notifications, unreadcount = client.get_notifications()

with open("data/seen_notifications.json", "r") as file:
    seen_ids = json.load(file)

print(seen_ids)

new_notifications = []

for notification in notifications[0:6]:
    if notification["id"] not in seen_ids:
        new_notifications.append(notification)

print("New notifications:", len(new_notifications))

for notification in new_notifications:
    print("--------------------")
    print("ID:", notification["id"])
    print("Subject:", notification["subject"])
    print("Content:", notification["smallmessage"])
    seen_ids.append(notification["id"])

print(seen_ids)
with open("data/seen_notifications.json", "w") as file:
    json.dump(seen_ids, file)