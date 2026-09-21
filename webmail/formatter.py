def format_email_notification(email):
    sender = email.get("from", "Unknown sender")
    subject = email.get("subject", "(No subject)")
    body = email.get("body", "")

    # Keep the WhatsApp notification reasonably short
    body = " ".join(body.split())

    if len(body) > 500:
        body = body[:500] + "..."

    return (
        "📧 New UoM Email\n\n"
        f"From: {sender}\n\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{body}"
    )

def get_template_parameters(email):
    sender = email.get("from", "Unknown sender")
    subject = email.get("subject", "(No subject)")
    body = email.get("body", "")

    body = " ".join(body.split())

    if len(body) > 500:
        body = body[:500] + "..."

    return [
        sender,
        subject,
        body,
    ]