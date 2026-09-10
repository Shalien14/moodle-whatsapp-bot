import os
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from moodle.notifications import fetch_notifications
load_dotenv()

class MoodleClient:
    def __init__(self):
        self.moodle_url = "https://online.uom.lk"
        self.login_url = f"{self.moodle_url}/login/index.php"

        self.username = os.getenv("MOODLE_USERNAME")
        self.password = os.getenv("MOODLE_PASSWORD")

        self.session = requests.Session()

        self.sesskey = None
        self.userid = None

    def login(self):
        response=self.session.get(self.login_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        logintoken = soup.find("input", {"name": "logintoken"})["value"]
        login_data = {
            "logintoken": logintoken,
            "username": self.username,
            "password": self.password,
        }

        response = self.session.post(
            self.login_url,
            data=login_data
        )
        response.raise_for_status()

        my_page = self.session.get(f"{self.moodle_url}/my/")
        my_page.raise_for_status()

        match = re.search(r'M\.cfg\s*=\s*(\{.*?\});', my_page.text)

        if not match:
            raise Exception("Moodle configuration not found")

        moodle_config = match.group(1)

        self.sesskey = re.search(
            r'"sesskey":"([^"]+)"',
            moodle_config
        ).group(1)

        self.userid = re.search(
            r'"userId":(\d+)',
            moodle_config
        ).group(1)

    def get_notifications(self):
        return fetch_notifications(
            self.session,
            self.sesskey,
            self.userid
        )