from email import message_from_bytes
from email.header import decode_header


def decode_text(value):

    if not value:
        return ""

    decoded = decode_header(value)

    result = ""

    for text, encoding in decoded:

        if isinstance(text, bytes):

            result += text.decode(
                encoding or "utf-8",
                errors="replace"
            )

        else:

            result += text

    return result


def extract_body(msg):

    body = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()

            content_disposition = str(
                part.get("Content-Disposition")
            )

            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):

                payload = part.get_payload(
                    decode=True
                )

                if payload:

                    body = payload.decode(
                        part.get_content_charset()
                        or "utf-8",
                        errors="replace"
                    )

                break

    else:

        payload = msg.get_payload(
            decode=True
        )

        if payload:

            body = payload.decode(
                msg.get_content_charset()
                or "utf-8",
                errors="replace"
            )

    return body


def parse_email(raw_email, uid):

    msg = message_from_bytes(raw_email)

    return {
        "uid": uid.decode() if isinstance(uid, bytes) else str(uid),
        "from": decode_text(msg.get("From")),
        "to": decode_text(msg.get("To")),
        "subject": decode_text(msg.get("Subject")),
        "date": msg.get("Date"),
        "body": extract_body(msg)
    }