import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from moodle.notifications import fetch_notifications

load_dotenv()

MOODLE_URL = "https://online.uom.lk"
LOGIN_URL = f"{MOODLE_URL}/login/index.php"

username = os.getenv("MOODLE_USERNAME")
password = os.getenv("MOODLE_PASSWORD")

session = requests.Session()

# Get login page
response = session.get(LOGIN_URL)
response.raise_for_status()

# Extract Moodle's login token
soup = BeautifulSoup(response.text, "html.parser")
logintoken = soup.find("input", {"name": "logintoken"})["value"]

# Submit login
login_data = {
    "logintoken": logintoken,
    "username": username,
    "password": password,
}

response = session.post(LOGIN_URL, data=login_data)

# Get the logged-in user's Moodle ID
my_page = session.get(f"{MOODLE_URL}/my/")
my_page.raise_for_status()
# Extract Moodle configuration
match = re.search(r'M\.cfg\s*=\s*(\{.*?\});', my_page.text)

if not match:
    raise Exception("Moodle configuration not found")

moodle_config = match.group(1)

sesskey = re.search(r'"sesskey":"([^"]+)"', moodle_config).group(1)
userid = re.search(r'"userId":(\d+)', moodle_config).group(1)

print("User ID:", userid)
print("Sesskey found:", bool(sesskey))

# print("Logged-in successfully")
# print("Status:", response.status_code)
# print("URL:", response.url)
# print("Cookies:", session.cookies.get_dict())

# Fetch Moodle notifications
notifications, unreadcount = fetch_notifications(
    session,
    sesskey,
    userid
)

print("Unread notifications:", unreadcount)
print("Total notifications:", len(notifications))

for notification in notifications:
    print("--------------------")
    print("ID:", notification["id"])
    print("Subject:", notification["subject"])
    print("Content:", notification["smallmessage"])
    print("Time:", notification["timecreatedpretty"])
    print("Read:", notification["read"])
    print("Type:", notification["eventtype"])
    print("URL:", notification["contexturl"])