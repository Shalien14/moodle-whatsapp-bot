
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_URL = "https://graph.facebook.com/v25.0"


def _get_config():
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    recipient = os.getenv("WHATSAPP_RECIPIENT")

    if not all([access_token, phone_number_id, recipient]):
        raise ValueError("Missing WhatsApp configuration in .env")

    return access_token, phone_number_id, recipient


def _send_request(data):
    access_token, phone_number_id, _ = _get_config()

    url = f"{GRAPH_URL}/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if not response.ok:
        print("WhatsApp API Error:")
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()
    return response.json()


def send_message(message):
    """
    Send a normal WhatsApp text message.
    Subject to the 24-hour customer-service window.
    """

    _, _, recipient = _get_config()

    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,
        },
    }

    return _send_request(data)


def send_template(template_name, language_code, parameters):
    """
    Send an approved WhatsApp template.
    """

    _, _, recipient = _get_config()

    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code,
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": " ".join(str(p).split()),
                        }
                        for p in parameters
                    ],
                }
            ],
        },
    }

    return _send_request(data)
