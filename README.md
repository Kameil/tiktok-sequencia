# TikTok TTSK ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

**TTSK (TikTok Streak Keeper)** is a Python tool that automatically maintains your TikTok conversation streaks by sending a message to your active chats once per day.

## Requirements

* Python 3.x
* Google Chrome (handled by [CloakBrowser](https://cloakbrowser.dev/))
* [uv](https://github.com/astral-sh/uv) (Python package manager)

## Installation

### Option 1: Pre-built Binary (recommended)

No Python or extra dependencies required. Download the latest release for your platform from the [releases page](https://github.com/Kameil/tiktok-ttsk/releases/latest) and run it directly.

### Option 2: From Source

```bash
git clone https://github.com/Kameil/tiktok-ttsk.git
cd tiktok-ttsk
uv sync
```

## Usage

### Binary

Run the downloaded executable directly.

### From Source

```bash
uv run python main.py
```

## How It Works

1. Opens TikTok in a browser using your saved session cookies
2. Navigates to the messages page
3. Sends a random message to each active conversation
4. Stores today's date to avoid running multiple times per day

On the **first run**, a browser window will open prompting you to log in to your TikTok account. After logging in, your session cookies are saved automatically — you may need to rerun the program once for the session to load properly. All subsequent runs will reuse the saved session without any manual intervention.

The tool runs **once per day**. If already executed on the current day, it will exit immediately without sending any messages.

> [!NOTE]
> Automating interactions may violate TikTok's Terms of Service and can result in account suspension or a permanent ban. Use at your own risk.
