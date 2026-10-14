from webmail.formatter import (
    format_email_notification,
    get_template_parameters,
)


email = {
    "uid": "475",
    "from": "Gamage C.D. Chandana (via LMS)",
    "to": "SHALIEN N. 250586A",
    "subject": "ICPC Sri Lanka 2026/27",
    "date": "Sun, 20 Sep 2026",
    "body": """
    A new message has been posted in your UoM course.
    Please check the Moodle discussion for more information.
    """,
}


print("----- NORMAL MESSAGE -----")
print(format_email_notification(email))

print("\n----- TEMPLATE PARAMETERS -----")
print(get_template_parameters(email))