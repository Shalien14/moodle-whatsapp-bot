# Moodle WhatsApp Bot

A Python-based bot that connects to Moodle and delivers Moodle notifications through WhatsApp.

The main goal of this project is to prevent important university Moodle notifications from being missed by providing a convenient way to access them through WhatsApp.

## 🚧 Project Status

**Currently in development**

The first version focuses on connecting to Moodle, authenticating a user, and retrieving Moodle notifications through Moodle's internal AJAX service.

WhatsApp integration is planned for a later stage.

## 🎯 Goals

- 🔐 Authenticate with Moodle
- 🔔 Retrieve Moodle notifications
- 📋 Parse and organize notification data
- 🆕 Detect new notifications
- 💾 Store notification history
- 📱 Deliver notifications through WhatsApp
- 💬 Allow users to query their Moodle notifications through WhatsApp

## 🏗️ Current Architecture

```text
Moodle
   │
   │ HTTP / AJAX
   ▼
Python Backend
   │
   ├── Authentication
   ├── Session Management
   └── Notification Retrieval
   │
   ▼
Notification Data
   │
   ▼
WhatsApp Bot
   │
   ▼
User