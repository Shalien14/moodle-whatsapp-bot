import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from moodle.notifications import fetch_notifications

load_dotenv()


# print("Unread notifications:", unreadcount)
# print("Total notifications:", len(notifications))

# for notification in notifications:
#     print("--------------------")
#     print("ID:", notification["id"])
#     print("Subject:", notification["subject"])
#     print("Content:", notification["smallmessage"])
#     print("Time:", notification["timecreatedpretty"])
#     print("Read:", notification["read"])
#     print("Type:", notification["eventtype"])
#     print("URL:", notification["contexturl"])
from moodle.client import MoodleClient

client = MoodleClient()

client.login()

notifications, unreadcount = client.get_notifications()

print("Unread notifications:", unreadcount)
print("Total notifications:", len(notifications))