import json
import os

from gmail.client import GmailClient
from storage import load_seen_email_uids, save_seen_email_uids


client = GmailClient()

try:
    client.login()

    gmail_uids = client.get_uids()
    existing_uids = load_seen_email_uids()

    existing_set = set(existing_uids)

    new_count = 0

    for uid in gmail_uids:
        if uid not in existing_set:
            existing_uids.append(uid)
            existing_set.add(uid)
            new_count += 1

    save_seen_email_uids(existing_uids)

    print()
    print("========== Gmail Seen-ID Initialization ==========")
    print(f"Gmail messages found : {len(gmail_uids)}")
    print(f"Already in seen file : {len(existing_uids) - new_count}")
    print(f"Added as seen        : {new_count}")
    print(f"Total seen IDs       : {len(existing_uids)}")
    print("===================================================")

finally:
    client.logout()