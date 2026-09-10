import os
import requests
from dotenv import load_dotenv

load_dotenv()

from whatsapp.sender import send_message

send_message("🔔 Test from my Moodle Bot!")