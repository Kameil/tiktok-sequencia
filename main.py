import os
import sys
import time
import pickle
import random
import platform
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from notifypy import Notify
from cloakbrowser import launch


def get_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    data_dir = base / "tiktok-ttsk"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_browser_args():
    if platform.system() == "Windows":
        return []
    if os.environ.get("WAYLAND_DISPLAY"):
        return ["--ozone-platform=wayland"]
    return ["--ozone-platform=x11"]


def wait_for_login(page):
    logger.info("Waiting for user to log in...")
    while True:
        try:
            url = page.url
            url_ok = "/login" not in url and "tiktok.com" in url and url != "https://www.tiktok.com/"
            dom_ok = page.query_selector('[data-e2e="recommend-list-item-container"]') is not None \
                  or page.query_selector('[data-e2e="browse-video"]') is not None \
                  or page.query_selector('[data-e2e="chat-list-item"]') is not None
            if url_ok or dom_ok:
                logger.info(f"Login detected. URL: {url}")
                return
        except Exception:
            pass
        time.sleep(1)


BASE_DIR = get_data_dir()
T_FILE = BASE_DIR / "t.txt"
COOKIES_FILE = BASE_DIR / "cookies.pkl"
LOG_FILE = BASE_DIR / "app.log"

handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

logger = logging.getLogger("TikTokTTSK")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.info(f"[info] Data directory: {BASE_DIR}")

today = datetime.now()
if T_FILE.exists():
    if T_FILE.read_text(encoding="utf-8") == str(today.day):
        logger.info("Already sent today.")
        ntf_reopen = Notify()
        ntf_reopen.title = "Already sent today"
        ntf_reopen.message = "Messages already sent today. Reopen the app tomorrow."
        ntf_reopen.send()
        time.sleep(5)
        sys.exit(0)

browser = launch(headless=False, args=get_browser_args())
context = browser.new_context()
page = context.new_page()
page.goto("https://www.tiktok.com/login")

if not COOKIES_FILE.exists():
    logger.info("No account found. Waiting for login...")

    ntf = Notify()
    ntf.title = "Login with your account"
    ntf.message = "Log in on the browser. The app will continue automatically."
    ntf.send()

    wait_for_login(page)

    time.sleep(2)
    cookies = context.cookies()
    pickle.dump(cookies, open(COOKIES_FILE, "wb"))
    logger.info(f"Cookies saved at: {COOKIES_FILE}")

    ntf2 = Notify()
    ntf2.title = "Login successful"
    ntf2.message = "Cookies saved! Reopen the app to start sending messages."
    ntf2.send()

    browser.close()
    time.sleep(1)
    sys.exit(0)

cookies = pickle.load(open(COOKIES_FILE, "rb"))
context.add_cookies(cookies)

page.reload()
time.sleep(1)
page.goto("https://www.tiktok.com/messages?lang=pt-BR")

page.wait_for_selector('[data-e2e="chat-list-item"]')

WORDS = [
    "desenrolado",
    "orea seca",
    "fogo",
    "sossegado",
    "feijao com farinha",
    "moleculas aahh",
]

conversation_items = page.query_selector_all('[data-e2e="chat-list-item"]')
total = len(conversation_items)
logger.info(f"{total} conversations found.")

for i in range(total):
    try:
        conversation_items = page.query_selector_all('[data-e2e="chat-list-item"]')
        conversation_items[i].click()
        logger.info(f"[{i + 1}/{total}] Conversation(s) opened.")

        page.wait_for_selector('[data-e2e="message-input-area"] [contenteditable="true"]')
        boxx = page.locator('[data-e2e="message-input-area"] [contenteditable="true"]')
        boxx.click()
        time.sleep(1)

        msg = random.choice(WORDS)
        page.keyboard.type(msg, delay=200)

        time.sleep(0.5)
        page.keyboard.press("Enter")
        logger.info(f"[{i + 1}/{total}] Sent: '{msg}'")
        time.sleep(2)

    except Exception as e:
        logger.error(f"[{i + 1}/{total}] Erro: {e}")
        continue

T_FILE.write_text(str(today.day), encoding="utf-8")
logger.info("All messages sent.")
browser.close()
