import json


NOTIFICATION_FILE = "data/seen_notifications.json"
EMAIL_FILE = "data/seen_emails.json"


def load_seen_ids():

    with open(NOTIFICATION_FILE, "r") as file:
        return json.load(file)


def save_seen_ids(seen_ids):

    with open(NOTIFICATION_FILE, "w") as file:
        json.dump(seen_ids, file)


def load_seen_email_uids():

    with open(EMAIL_FILE, "r") as file:
        return json.load(file)


def save_seen_email_uids(seen_uids):

    with open(EMAIL_FILE, "w") as file:
        json.dump(seen_uids, file)