# Moodle WhatsApp Bot

A personal Python project that forwards university email notifications to WhatsApp, helping prevent important Moodle announcements and updates from being missed.

What started as a simple idea to solve a notification problem evolved into a project exploring web scraping, API integration, email processing, OAuth authentication, automation, and cloud deployment.

## ✨ Features

- 📧 Retrieve messages from Gmail using the Gmail API.
- 🔎 Filter messages using a configured Gmail label.
- 📨 Parse email senders, subjects, and message content.
- 🆕 Detect previously unseen email messages.
- 📱 Deliver notifications through the WhatsApp Business Platform.
- 💾 Track processed message IDs to reduce duplicate notifications.
- 🔁 Automatically check for new messages at regular intervals.
- 🧪 Include tests for email retrieval, parsing, formatting, and WhatsApp integration.

## 🏗️ Architecture

The project evolved from direct Moodle notification retrieval to using university email as the notification source.

The current implementation follows this workflow:

```text
University Email Notifications
              │
              ▼
            Gmail
          Gmail API
              │
              ▼
        Python Application
              │
       ┌──────┴──────┐
       ▼             ▼
  Email Parsing   ID Tracking
       │             │
       └──────┬──────┘
              ▼
       WhatsApp Sender
              │
              ▼
       WhatsApp Business
              │
              ▼
             User
```

### Technology stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Email integration | Gmail API |
| Authentication | Google OAuth 2.0 |
| HTTP requests | Requests |
| Email parsing | Python email processing and BeautifulSoup |
| WhatsApp delivery | WhatsApp Business Platform / Meta Graph API |
| Local state | JSON files |
| Logging | Python logging |
| Progress display | tqdm |
| Deployment experience | Microsoft Azure VM |

## 📂 Project Structure

```text
moodle-whatsapp-bot/
├── gmail/                 # Gmail API integration
├── moodle/                # Original Moodle integration
├── tests/                 # Tests and integration checks
├── webmail/               # Email parsing and formatting
├── webpage/               # Project web pages
├── whatsapp/              # WhatsApp message delivery
├── .gitignore
├── README.md
├── logger.py              # Logging configuration
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── storage.py              # Processed-message state
```

Private credentials, OAuth tokens, virtual environments, logs, and local notification-state files should not be committed to the repository.

## ⚙️ Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version.
- A Google account with Gmail API access.
- A Google Cloud project with the Gmail API enabled.
- Google OAuth credentials configured for the application.
- A Meta developer application with WhatsApp Business Platform access.
- An approved WhatsApp message template compatible with the application.

### 1. Clone the repository

```bash
git clone https://github.com/Shalien14/moodle-whatsapp-bot.git
cd moodle-whatsapp-bot
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment using:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gmail API access

1. Create or select a project in Google Cloud Console.
2. Enable the Gmail API.
3. Configure the OAuth consent screen.
4. Create OAuth client credentials appropriate for a local application.
5. Save the downloaded client credentials as `credentials.json` in the project root.
6. Configure the Gmail label used by the application in `gmail/client.py`.

On the first authenticated run, the application may open a browser to complete OAuth authorization and create `token.json`.

**Keep `credentials.json` and `token.json private.** Never commit them to GitHub or share their contents.

Google OAuth publishing and authorization requirements depend on the consent-screen configuration and the scopes being requested.

### 5. Configure WhatsApp

Create a `.env` file in the project root with your own Meta WhatsApp configuration:

```dotenv
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_RECIPIENT=your_recipient_number
```

Replace the placeholders with your actual values. Do not commit `.env` to Git.

Configure the approved WhatsApp message template and its language to match the application. The current implementation uses the `new_uom_email` template with three text parameters: sender, subject, and message preview.

### 6. Run the bot

```bash
python main.py
```

The application checks for new messages approximately every ten minutes. It records successfully processed message IDs in local runtime state so previously processed messages can be skipped on subsequent checks.

**Important:** Keep the runtime-state files available if you want to preserve deduplication between restarts. Starting without the previous state can cause old messages to be processed again.

## 🧪 Testing

The repository includes tests for different parts of the project, including Gmail access, email parsing, formatting, notification tracking, and WhatsApp integration.

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

Some tests may require valid credentials, network access, or external service configuration. Review individual test files before running tests that contact live services or send WhatsApp messages.

## ⚠️ Limitations

- The application depends on Google OAuth authorization and Gmail API availability.
- WhatsApp delivery requires valid Meta credentials and compatible message templates.
- WhatsApp messaging is subject to Meta's messaging policies, including customer-service window and template requirements.
- The application uses local JSON files for message tracking rather than a dedicated database.
- Email content is forwarded to WhatsApp, so users should consider privacy and the sensitivity of the messages being processed.
- The project was developed for personal use and learning; it is not presented as a production-grade notification service.

## 🔐 Security and Privacy

- Never commit OAuth tokens, client credentials, access tokens, or `.env` files.
- Avoid publishing personal email content, recipient identifiers, or notification history.
- Use a dedicated environment for testing integrations that send real messages.
- Revoke exposed credentials and rotate tokens if they are accidentally published.
- Review the project's [privacy information](webpage/privacy.html) before using or adapting the application.

## 💡 Project Origin

This project was inspired by a real problem raised by a friend who often missed important Moodle notifications.

What began as a simple idea for another group project eventually became a personal project to explore a practical solution.

**Original idea and inspiration:** [Luxshagini](https://github.com/Luxshagini)

Thanks for the idea that sparked this project! ❤️

## 🎓 What I Learned

Building this project gave me practical experience with:

- Python application design and modular code organization.
- Moodle and webmail integration.
- Gmail API integration and OAuth authentication.
- Email parsing and message deduplication.
- WhatsApp Business Platform integration.
- Environment variables and credential management.
- Logging, testing, and troubleshooting.
- Deploying and debugging applications on a Linux Azure VM.

## 📌 Project Status

This repository documents a personal learning project and its development journey. It is shared publicly for educational purposes, experimentation, and reference.

The project is not guaranteed to be actively maintained or continuously running.

---

Made with curiosity, Python, and a desire to stop missing university notifications. 🤣
