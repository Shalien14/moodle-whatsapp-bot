import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_URL = "https://graph.facebook.com/v25.0"


def _headers():
    return {
        "Authorization": f"Bearer {os.getenv('WHATSAPP_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }


def _url():
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    return f"{GRAPH_URL}/{phone_number_id}/messages"


def send_message(message):
    """
    Send a normal WhatsApp text message.
    Intended for messages sent inside the WhatsApp customer-service window.
    """

    recipient = os.getenv("WHATSAPP_RECIPIENT")

    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message,
        },
    }

    response = requests.post(
        _url(),
        headers=_headers(),
        json=data,
        timeout=30,
    )

    print("WhatsApp template response:", response.status_code)

    response.raise_for_status()

    return response.json()


def send_template(template_name, language_code, parameters):
    """
    Send an approved WhatsApp template.
    """

    recipient = os.getenv("WHATSAPP_RECIPIENT")

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
                            "text": " ".join(str(parameter).split()),
                        }
                        for parameter in parameters
                    ],
                }
            ],
        },
    }

    response = requests.post(
        _url(),
        headers=_headers(),
        json=data,
        timeout=30,
    )

    print("WhatsApp template response:", response.status_code)
    # print("WhatsApp template response body:", response.text)

    response.raise_for_status()

    return response.json()
