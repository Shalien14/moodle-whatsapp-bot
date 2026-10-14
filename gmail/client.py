from pathlib import Path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailClient:

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly"
    ]

    LABEL_NAME = "shalienn.25@uom.lk"

    BASE_DIR = Path(__file__).resolve().parent.parent

    CREDENTIALS_FILE = BASE_DIR / "credentials.json"
    TOKEN_FILE = BASE_DIR / "token.json"

    def __init__(self):
        self.service = None
        self.mail = None

    def connect(self):

        print("Connecting to Gmail...")

        creds = None

        if self.TOKEN_FILE.exists():

            creds = Credentials.from_authorized_user_file(
                str(self.TOKEN_FILE),
                self.SCOPES
            )

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

            with open(self.TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.CREDENTIALS_FILE),
                self.SCOPES
            )

            creds = flow.run_local_server(port=0)

            with open(self.TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        self.service = build(
            "gmail",
            "v1",
            credentials=creds
        )

        self.mail = self.service

        print("Connected to Gmail! 📧")

    def login(self):

        if self.service is None:
            self.connect()

        print("Gmail authentication successful! 🎉")

    def select_inbox(self):

        if self.service is None:
            self.connect()

        response = self.service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=1
        ).execute()

        return response.get(
            "resultSizeEstimate",
            0
        )

    def get_uids(self):

        if self.service is None:
            self.connect()

        label_id = self._get_label_id()

        message_ids = []

        response = self.service.users().messages().list(
            userId="me",
            labelIds=[label_id],
            maxResults=100
        ).execute()

        while True:

            for message in response.get("messages", []):
                message_ids.append(message["id"])

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

            response = self.service.users().messages().list(
                userId="me",
                labelIds=[label_id],
                maxResults=100,
                pageToken=next_page_token
            ).execute()

        return message_ids

    def fetch_email(self, uid):

        if self.service is None:
            self.connect()

        message = self.service.users().messages().get(
            userId="me",
            id=uid,
            format="raw"
        ).execute()

        raw_email = base64.urlsafe_b64decode(
            message["raw"] + "=="
        )

        return raw_email

    def logout(self):

        self.service = None
        self.mail = None

        print("Logged out.")

    def _get_label_id(self):

        response = self.service.users().labels().list(
            userId="me"
        ).execute()

        for label in response.get("labels", []):

            if label["name"] == self.LABEL_NAME:
                return label["id"]

        raise Exception(
            f"Gmail label '{self.LABEL_NAME}' not found"
        )