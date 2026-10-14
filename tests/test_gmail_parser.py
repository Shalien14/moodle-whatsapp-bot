from gmail.client import GmailClient
from webmail.emails import parse_email


client = GmailClient()

client.login()

uids = client.get_uids()

print(f"Found {len(uids)} inbox messages")

if not uids:
    print("No emails found.")
    client.logout()
    exit()

uid = uids[0]

print(f"Testing Gmail message ID: {uid}")

raw_email = client.fetch_email(uid)

print(f"Raw email size: {len(raw_email)} bytes")

email_data = parse_email(
    raw_email,
    uid
)

print("\n========== PARSED EMAIL ==========")

print("UID:", email_data["uid"])
print("From:", email_data["from"])
print("To:", email_data["to"])
print("Subject:", email_data["subject"])
print("Date:", email_data["date"])

print("\nBody:")
print(email_data["body"][:1000])

print("\n===================================")

client.logout()