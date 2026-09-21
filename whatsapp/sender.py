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

    response.raise_for_status()

    print("WhatsApp text sent:", response.status_code)

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
                            "text": str(parameter),
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

    response.raise_for_status()

    print("WhatsApp template sent:", response.status_code)

    return response.json()