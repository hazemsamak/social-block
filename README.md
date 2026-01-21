
# PiHole Social Control

A premium web interface to easily block and unblock specific clients (e.g., kids' devices) from accessing specific content groups (e.g., Social Media) on your Pi-hole.

![UI Screenshot](https://via.placeholder.com/800x400?text=Premium+Dark+UI) *Note: Add actual screenshot here*

## Features

- **One-Click Toggle**: Enable (Block) or Disable (Unblock) access instantly.
- **Pi-hole Integration**: Automatically manages Pi-hole Groups and Clients.
- **Discord Notifications**: Sends status updates to your Discord server unique webhooks.
- **Premium UI**: Modern, dark-mode design with responsive interactions.
- **Docker Support**: Easy deployment with Docker Compose.

## Prerequisites

- A running Pi-hole instance (v5/v6).
- A Discord Webhook URL.
- Python 3.9+ or Docker.

## Installation

### Option 1: Docker (Recommended)

1.  Clone the repository.
2.  Create a `.env` file (see Configuration).
3.  Run:
    ```bash
    docker-compose up -d --build
    ```
4.  Open `http://localhost:5000`.

### Option 2: Manual

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python app.py
    ```

## Configuration

Create a `.env` file in the root directory:

```ini
PIHOLE_URL=http://192.168.1.100:8000
PIHOLE_PASSWORD=your_pihole_password
DISCORD_WEBHOOK_URL=your_discord_webhook_url
CLIENT_IP=192.168.1.0/24
```

## How It Works

- **Blocking**: Enables the "Social" group in Pi-hole and adds the target Client IP to that group.
- **Unblocking**: Disables the "Social" group and removes the Client IP.

## License

MIT
