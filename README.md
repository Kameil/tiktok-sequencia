# TikTok TTSK ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

**TTSK (TikTok Streak Keeper)** is a Python tool that automatically maintains your TikTok conversation streaks by sending a message to your active chats once per day.

## Requirements

* Python 3.x
* Google Chrome (handled by [CloackBrowser](https://cloakbrowser.dev/))
* [uv](https://github.com/astral-sh/uv) (Python package manager)

## Installation

```bash
git clone https://github.com/Kameil/tiktok-ttsk.git
cd tiktok-ttsk
uv sync
```

## Usage

```bash
uv run python main.py
```

On the first run, a browser window will open and prompt you to log in to your TikTok account.

After logging in, it will automatically save the cookies and you may need to rerun the program for it to load your session cookies.
Future runs will automatically reuse the saved session.

The tool runs **once per day**. If it has already been executed on the same day, it will exit without sending messages.

## How It Works

1. Opens TikTok in a browser using your saved session cookies
2. Navigates to the messages page
3. Sends a random message to each active conversation
4. Stores today's date to avoid running multiple times per day

> [!WARNING]
> For educational and research purposes only. Automating interactions may violate TikTok's Terms of Service and can result in account suspension or a permanent ban. Use at your own risk.
