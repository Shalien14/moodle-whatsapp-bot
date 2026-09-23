from gmail.client import GmailClient
from storage import load_seen_email_uids


client = GmailClient()

try:
    client.login()

    uids = client.get_uids()
    seen_uids = load_seen_email_uids()

    new_uids = [
        uid
        for uid in uids
        if uid not in seen_uids
    ]

    print()
    print("========== Gmail New Email Test ==========")
    print(f"Total Gmail messages : {len(uids)}")
    print(f"Previously seen      : {len(seen_uids)}")
    print(f"New messages         : {len(new_uids)}")

    if new_uids:
        print("\nNew IDs:")
        for uid in new_uids:
            print(uid)
    else:
        print("\n✅ No new messages. Safe to start the bot.")

    print("===========================================")

finally:
    client.logout()