import os
import requests
from chat import chat


# info on verification request payload: https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(token, mode):
    if token == os.getenv("VERIFY_TOKEN") and mode == "subscribe":
        return True
    else:
        return False


def webhook(request):
    data = parse_webhook_payload(request)
    if data:
        response = chat(data["message"])
        send_message(data["phone_number_id"], data["from_number"], response)
        return True
    else:
        return False


def parse_webhook_payload(body):
    # whatsapp sends payloads for various things, we just want to ignore
    # unless it's a message with text
    # info on WhatsApp text message payload: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
    try:
        return {
            "phone_number_id": body["entry"][0]["changes"][0]["value"]["metadata"][
                "phone_number_id"
            ],
            "from_number": body["entry"][0]["changes"][0]["value"]["messages"][0][
                "from"
            ],
            "message": body["entry"][0]["changes"][0]["value"]["messages"][0]["text"][
                "body"
            ],
        }
    except KeyError:
        return None


def send_message(from_id, to, body):
    url = f'https://graph.facebook.com/v12.0/{from_id}/messages?access_token={os.getenv("WHATSAPP_TOKEN")}'

    requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "messaging_product": "whatsapp",
            "to": to,
            "text": {"body": "Ack: " + body},
        },
    )
