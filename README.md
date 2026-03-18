# TikTok Sequência (TTKS)

A Python tool that automatically maintains your TikTok conversation streaks by sending messages to all your active chats once per day.

## Requirements

- Python 3.x
- Google Chrome (handled by [CloackBrowser](https://cloakbrowser.dev/))
- [uv](https://github.com/astral-sh/uv) (package manager)

## Installation

```bash
git clone https://github.com/Kameil/tiktok-sequencia.git
cd tiktok-sequencia
uv sync
```

## Usage

```bash
uv run python main.py
```

On first run, a browser window will open and prompt you to log in to your TikTok account. Once logged in, press **Ctrl+S** to save your session cookies. Subsequent runs will use the saved session automatically.

The tool runs once per day — if it has already been executed today, it will exit immediately without sending any messages.

## How it works

1. Opens TikTok in a browser using your saved cookies
2. Navigates to your messages page
3. Sends a random message to each conversation
4. Records today's date to prevent duplicate runs

> [!WARNING]
> For educational and research purposes only. Automating interactions may violate TikTok's Terms of Service and can result in account suspension or a permanent ban. Use at your own risk.
