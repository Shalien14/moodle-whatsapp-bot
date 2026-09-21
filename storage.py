import json
import os


NOTIFICATION_FILE = "data/seen_notifications.json"
EMAIL_FILE = "data/seen_emails.json"


def _load_json_list(path):
    if not os.path.exists(path):
        return []

    with open(path, "r") as file:
        return json.load(file)


def _save_json_list(path, values):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as file:
        json.dump(values, file)


def load_seen_ids():
    return _load_json_list(NOTIFICATION_FILE)


def save_seen_ids(seen_ids):
    _save_json_list(NOTIFICATION_FILE, seen_ids)


def load_seen_email_uids():
    return _load_json_list(EMAIL_FILE)


def save_seen_email_uids(seen_uids):
    _save_json_list(EMAIL_FILE, seen_uids)