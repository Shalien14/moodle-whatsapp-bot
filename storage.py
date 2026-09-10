import json
def load_seen_ids():
    with open("data/seen_notifications.json", "r") as file:
        return json.load(file)

def save_seen_ids(seen_ids):
    with open("data/seen_notifications.json","w") as file:
        json.dump(seen_ids, file)