<div align="center">
  <h1>🤖 Telegram Username Parser</h1>

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

<div align="center">
    <b>English</b> |
    <a href="/README.ru.md">Русский</a>
</div>

## 📋 Overview

Telegram Username Parser is a tool that extracts usernames from Telegram channels and message history. It provides an efficient way to collect usernames from both channel participants and message authors.

## ✨ Features

- 🔍 Extract usernames from channel participants
- 📃 Parse usernames from message history
- 💾 Save results to a file
- 🔄 Prevent duplicates in results
- 🔐 Use Telegram API with session management

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/goldpulpy/telegram-username-parser.git
   cd telegram-username-parser
   ```

2. Install dependencies using Makefile:

   ```bash
   make setup
   ```

   This will create a virtual environment and install all necessary dependencies.

3. Configure Telegram API credentials:
   - Edit `config.json` and add:
     - `api_id`: Your Telegram API ID
     - `api_hash`: Your Telegram API hash
     - `phone`: Your phone number in international format

## 🛠️ Configuration

Create or edit the `config.json` file:

```json
{
  "api_id": YOUR_API_ID,
  "api_hash": "YOUR_API_HASH",
  "phone": "+YOUR_PHONE_NUMBER"
}
```

> ⚠️ **Note**: To obtain `api_id` and `api_hash`, register your application at [https://my.telegram.org/apps](https://my.telegram.org/apps)

## 🖥️ Usage

Run the main script:

```bash
source venv/bin/activate
python main.py
```

### Command-line arguments:

- `--config`: Path to the configuration file (default: `config.json`)
- `--result_directory`: Path to store results (default: `result`)
- `--session_directory`: Path to store sessions (default: `sessions`)
- `--debug`: Enable debug mode (optional)

## 📊 How It Works

1. The tool connects to Telegram using your credentials
2. Requests the target username of the channel or chat
3. First extracts usernames from chat/channel participants
4. Then analyzes message history to extract usernames of message authors
5. All unique usernames are saved to a file (in the format `@username`)

> ⚠️ **Note**: If collecting from a channel, the bot must be in the channel and have access to participants.

## 🧩 Architecture

The project is organized into several modules:

| Module           | Description                         |
| ---------------- | ----------------------------------- |
| `app/config.py`  | Configuration loading functionality |
| `app/parser.py`  | Username parsing strategies         |
| `app/result.py`  | Result storage and management       |
| `app/session.py` | Telegram session handling           |
| `main.py`        | Main entry point                    |

## 📝 License

This project is available under the [MIT](LICENSE) license.

<h6 align="center">Created by goldpulpy with ❤️</h6>
