import os
import imaplib
import ssl
import certifi
import email

from dotenv import load_dotenv
from email.header import decode_header

load_dotenv()

USERNAME = os.getenv("UOM_USERNAME")
PASSWORD = os.getenv("UOM_PASSWORD")

IMAP_SERVER = "mail.uom.lk"
IMAP_PORT = 993


def decode_text(value):
    if not value:
        return ""

    decoded = decode_header(value)
    result = ""

    for text, encoding in decoded:
        if isinstance(text, bytes):
            result += text.decode(encoding or "utf-8", errors="replace")
        else:
            result += text

    return result


print("Connecting to UoM mail...")

context = ssl.create_default_context(
    cafile=certifi.where()
)

# UoM IMAP server uses a legacy 1024-bit DH parameter.
context.set_ciphers("DEFAULT:@SECLEVEL=1")

mail = imaplib.IMAP4_SSL(
    IMAP_SERVER,
    IMAP_PORT,
    ssl_context=context
)

print("Connected!")

print("Logging in...")

mail.login(USERNAME, PASSWORD)

print("Login successful! 🎉")

status, messages = mail.select("INBOX")

if status != "OK":
    print("Failed to open inbox.")
    mail.logout()
    exit()

total_messages = int(messages[0])

print(f"Messages in INBOX: {total_messages}")

# Get the latest email
status, data = mail.fetch(
    str(total_messages),
    "(RFC822)"
)

if status != "OK":
    print("Failed to fetch email.")
    mail.logout()
    exit()

raw_email = data[0][1]

msg = email.message_from_bytes(raw_email)

print("\n" + "=" * 50)
print("LATEST EMAIL")
print("=" * 50)

print("From:", decode_text(msg.get("From")))
print("To:", decode_text(msg.get("To")))
print("Subject:", decode_text(msg.get("Subject")))
print("Date:", msg.get("Date"))

# Extract body
body = ""

if msg.is_multipart():

    for part in msg.walk():

        content_type = part.get_content_type()
        content_disposition = str(
            part.get("Content-Disposition")
        )

        if content_type == "text/plain" and "attachment" not in content_disposition:

            payload = part.get_payload(decode=True)

            if payload:
                body = payload.decode(
                    part.get_content_charset() or "utf-8",
                    errors="replace"
                )

            break

else:

    payload = msg.get_payload(decode=True)

    if payload:
        body = payload.decode(
            msg.get_content_charset() or "utf-8",
            errors="replace"
        )

print("\nBody:")
print(body[:2000])

print("=" * 50)

mail.logout()

print("\nLogged out.")