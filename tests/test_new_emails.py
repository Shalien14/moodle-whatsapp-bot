from webmail.client import WebmailClient
from webmail.emails import parse_email

from storage import (
    load_seen_email_uids,
    save_seen_email_uids
)


client = WebmailClient()

client.login()

client.select_inbox()

uids = client.get_uids()

# Convert bytes → strings
uids = [
    uid.decode()
    for uid in uids
]

seen_uids = load_seen_email_uids()

print(f"Total emails: {len(uids)}")
print(f"Previously seen: {len(seen_uids)}")

new_uids = [
    uid
    for uid in uids
    if uid not in seen_uids
]

print(f"New emails: {len(new_uids)}")


for uid in new_uids:

    print("\n" + "-" * 50)

    print(f"New email detected! UID: {uid}")

    raw_email = client.fetch_email(
        uid.encode()
    )

    email_data = parse_email(
        raw_email,
        uid
    )

    print("From:", email_data["from"])
    print("Subject:", email_data["subject"])
    print("Date:", email_data["date"])


# Save all currently known UIDs
save_seen_email_uids(uids)

client.logout()