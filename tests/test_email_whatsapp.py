from webmail.client import WebmailClient
from webmail.emails import parse_email
from whatsapp.sender import send_message

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

# First-run protection
if not seen_uids:

    print("First run detected.")
    print("Marking existing emails as seen...")

    save_seen_email_uids(uids)

    client.logout()

    print("Ready. Existing emails will not be sent to WhatsApp.")
    exit()


new_uids = [
    uid
    for uid in uids
    if uid not in seen_uids
]

print(f"New emails: {len(new_uids)}")


for uid in new_uids:

    print("\n" + "-" * 50)

    raw_email = client.fetch_email(
        uid.encode()
    )

    email_data = parse_email(
        raw_email,
        uid
    )

    print("UID:", email_data["uid"])
    print("From:", email_data["from"])
    print("Subject:", email_data["subject"])

    message = (
        "📧 *New UoM Email*\n\n"
        f"👤 From: {email_data['from']}\n\n"
        f"📌 Subject: {email_data['subject']}\n\n"
        f"🕒 {email_data['date']}\n\n"
        f"{email_data['body'][:3000]}"
    )

    send_message(message)

    print("WhatsApp message sent! 📱")


# Save UIDs after successful processing
save_seen_email_uids(uids)

client.logout()