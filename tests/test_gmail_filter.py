from gmail.client import GmailClient


client = GmailClient()
client.login()

# Get all Gmail labels
labels_response = client.service.users().labels().list(
    userId="me"
).execute()

labels = labels_response.get("labels", [])

label_id = None

for label in labels:
    if label["name"] == "shalienn.25@uom.lk":
        label_id = label["id"]
        break

if not label_id:
    print("❌ Label not found!")
    client.logout()
    exit()

print(f"Label found!")
print(f"Label ID: {label_id}")

response = client.service.users().messages().list(
    userId="me",
    labelIds=[label_id],
    maxResults=20
).execute()

messages = response.get("messages", [])

print(f"Messages in label: {len(messages)}")

for message in messages:
    msg = client.service.users().messages().get(
        userId="me",
        id=message["id"],
        format="metadata",
        metadataHeaders=["From", "Subject"]
    ).execute()

    headers = msg["payload"].get("headers", [])

    sender = next(
        (
            h["value"]
            for h in headers
            if h["name"].lower() == "from"
        ),
        "(unknown)"
    )

    subject = next(
        (
            h["value"]
            for h in headers
            if h["name"].lower() == "subject"
        ),
        "(no subject)"
    )

    print(f"\nFrom: {sender}")
    print(f"Subject: {subject}")
    print(f"ID: {message['id']}")

client.logout()