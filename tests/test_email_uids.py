from webmail.client import WebmailClient
from webmail.emails import parse_email


client = WebmailClient()

client.login()

total = client.select_inbox()

print(f"Messages in INBOX: {total}")

uids = client.get_uids()

print(f"Total UIDs: {len(uids)}")

print("\nLatest 5 emails:\n")

for uid in uids[-5:]:

    raw_email = client.fetch_email(uid)

    email_data = parse_email(
        raw_email,
        uid
    )

    print("-" * 50)

    print("UID:", email_data["uid"])
    print("From:", email_data["from"])
    print("Subject:", email_data["subject"])
    print("Date:", email_data["date"])

client.logout()