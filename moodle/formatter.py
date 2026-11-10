
import re
import html
from bs4 import BeautifulSoup


MAX_MESSAGE_LENGTH = 700


def extract_course_name(notification):
    """
    Extract the course name from Moodle notification HTML.
    """

    message_html = notification.get("fullmessagehtml", "")

    if message_html:
        soup = BeautifulSoup(message_html, "html.parser")

        for link in soup.find_all("a", href=True):
            if "/course/view.php" in link["href"]:
                course_name = link.get_text(" ", strip=True)

                if course_name:
                    return course_name

    # Fallback: extract course name from plain text.
    full_message = notification.get("fullmessage", "")

    match = re.search(
        r"\bin the course\s+(.+?)(?:\s*\[\d+\]|[.\n]|$)",
        full_message,
        re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return "General Moodle Notification"


def clean_message(notification):
    """
    Clean Moodle notification preview.
    """

    message = notification.get("smallmessage", "")

    message = html.unescape(message)

    message = re.sub(
        r"Change your notification preferences.*$",
        "",
        message,
        flags=re.IGNORECASE | re.DOTALL,
    )

    message = " ".join(message.split())

    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH - 3] + "..."

    return message or "You have a new Moodle notification."


def format_notification(notification):
    """
    Return the three parameters required by
    the new_moodle_notification WhatsApp template.
    """

    course = extract_course_name(notification)

    subject = html.unescape(
        notification.get("subject", "Moodle Notification")
    )

    message = clean_message(notification)

    return [
        course,
        subject,
        message,
    ]
