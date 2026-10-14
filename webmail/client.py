import os
import imaplib
import ssl
import certifi

from dotenv import load_dotenv

load_dotenv()


class WebmailClient:

    IMAP_SERVER = "mail.uom.lk"
    IMAP_PORT = 993

    def __init__(self):
        self.username = os.getenv("UOM_USERNAME")
        self.password = os.getenv("UOM_PASSWORD")
        self.mail = None

    def connect(self):

        print("Connecting to UoM mail...")

        context = ssl.create_default_context(
            cafile=certifi.where()
        )

        # Compatibility with the UoM IMAP server's
        # legacy 1024-bit DH parameter.
        context.set_ciphers("DEFAULT:@SECLEVEL=1")

        self.mail = imaplib.IMAP4_SSL(
            self.IMAP_SERVER,
            self.IMAP_PORT,
            ssl_context=context
        )

        print("Connected!")

    def login(self):

        if self.mail is None:
            self.connect()

        print("Logging in...")

        self.mail.login(
            self.username,
            self.password
        )

        print("Login successful! 🎉")

    def select_inbox(self):

        status, messages = self.mail.select("INBOX")

        if status != "OK":
            raise Exception("Failed to open INBOX")

        return int(messages[0])

    def get_uids(self):

        status, data = self.mail.uid(
            "SEARCH",
            None,
            "ALL"
        )

        if status != "OK":
            raise Exception("Failed to retrieve email UIDs")

        return data[0].split()

    def fetch_email(self, uid):

        status, data = self.mail.uid(
            "FETCH",
            uid,
            "(RFC822)"
        )

        if status != "OK":
            raise Exception(
                f"Failed to fetch email UID {uid.decode()}"
            )

        return data[0][1]

    def logout(self):

        if self.mail:
            self.mail.logout()
            self.mail = None

            print("Logged out.")