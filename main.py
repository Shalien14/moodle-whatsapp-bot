import time
from tqdm import tqdm
from gmail.client import GmailClient
from webmail.emails import parse_email

from whatsapp.sender import send_template

from storage import (
    load_seen_email_uids,
    save_seen_email_uids,
)

from logger import setup_logger


CHECK_INTERVAL = 600       # 10 minutes
RETRY_INTERVAL = 60        # 1 minute


logger = setup_logger()


def check_emails(client):
    """
    Check Gmail for new emails and send notifications.
    """


    uids = client.get_uids()

    seen_uids = load_seen_email_uids()

    new_uids = [
        uid
        for uid in uids
        if uid not in seen_uids
    ]

    logger.info(
        "Total emails: %d | Previously seen: %d | New emails: %d",
        len(uids),
        len(seen_uids),
        len(new_uids),
    )

    for uid in new_uids:

        logger.info("Processing new email UID: %s", uid)

        try:
            raw_email = client.fetch_email(uid)

            email_data = parse_email(
                raw_email,
                uid
            )

            logger.info(
                "Email: From=%s | Subject=%s",
                email_data["from"],
                email_data["subject"],
            )

            preview = email_data["body"].strip()
            if len(preview) > 500:
                preview = preview[:497] + "..."

            send_template(
                "new_uom_email",
                "en",
                [
                    email_data["from"],
                    email_data["subject"],
                    preview,
                ],
            )

            # Only mark as seen after successful delivery
            seen_uids.append(uid)

            logger.info(
                "Notification delivered successfully: UID %s",
                uid,
            )

        except Exception:
            logger.exception(
                "Failed to process email UID %s",
                uid,
            )

    save_seen_email_uids(seen_uids)


def wait_for_next_check():
    """
    Wait until the next Webmail check.
    """

    logger.info(
        "Waiting %d minutes until next check...",
        CHECK_INTERVAL // 60,
    )

    for _ in tqdm(
        range(CHECK_INTERVAL),
        desc="Waiting",
        unit="s",
    ):
        time.sleep(1)


def main():

    logger.info("Starting UoM Gmail bot")

    client = GmailClient()

    while True:

        try:

            # Connect if necessary
            if client.mail is None:
                logger.info("Connecting to Gmail...")
                client.login()

            check_emails(client)

            wait_for_next_check()

        except KeyboardInterrupt:

            logger.info("Stopping UoM Gmail bot...")
            break

        except Exception:

            logger.exception("Gmail check failed")

            logger.info(
                "Retrying in %d seconds...",
                RETRY_INTERVAL,
            )

            # Drop the current connection.
            # The next iteration will create a fresh one.
            try:
                client.logout()
            except Exception:
                pass

            time.sleep(RETRY_INTERVAL)

    try:
        client.logout()
    except Exception:
        pass

    logger.info("Bot stopped.")


if __name__ == "__main__":
    main()