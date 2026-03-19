import os
import time
import pickle
import random
import threading
from datetime import datetime
from pathlib import Path
from notifypy import Notify
from pynput import keyboard as pynput_keyboard
from cloakbrowser import launch


def get_data_dir() -> Path:
    """
    Returns a persistent directory for storing app data.
    - Linux: ~/.local/share/tiktok-sequencia/
    - Windows: %APPDATA%/tiktok-sequencia/
    """
    if os.name == "nt":  # Windows
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:  # Linux/macOS
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    data_dir = base / "tiktok-sequencia"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


BASE_DIR = get_data_dir()
T_FILE = BASE_DIR / "t.txt"
COOKIES_FILE = BASE_DIR / "cookies.pkl"

print(f"[info] Data directory: {BASE_DIR}")

# Verify if it is already sent
today = datetime.now()
if T_FILE.exists():
    if T_FILE.read_text(encoding="utf-8") == str(today.day):
        print("Already sent today.")
        time.sleep(5)
        exit()

# Initialize browser
browser = launch(headless=False, args=["--ozone-platform=x11"])
context = browser.new_context()
page = context.new_page()
page.goto("https://tiktok.com/")

# Save cookies if not found
if not COOKIES_FILE.exists():
    print("No account found. Please log in and press Ctrl+S to save your cookies.")

    ntf = Notify()
    ntf.title = "Login with your account"
    ntf.message = "No account found. Please log in and save your cookies."
    ntf.send()

    pressed_keys = set()
    save_event = threading.Event()
    stop_event = threading.Event()

    def on_press(key):
        pressed_keys.add(key)
        ctrl_held = {pynput_keyboard.Key.ctrl_l, pynput_keyboard.Key.ctrl_r} & pressed_keys
        if key == pynput_keyboard.KeyCode.from_char('s') and ctrl_held:
            save_event.set()

    def on_release(key):
        pressed_keys.discard(key)
        if key == pynput_keyboard.Key.esc:
            stop_event.set()
            return False

    print("Press Esc to exit or Ctrl+S to save cookies.")
    with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not stop_event.is_set():
            if save_event.is_set():
                cookies = context.cookies()
                pickle.dump(cookies, open(COOKIES_FILE, "wb"))
                print(f"Cookies saved at: {COOKIES_FILE}")
                ntf2 = Notify()
                ntf2.title = "Cookies saved"
                ntf2.message = "Cookies saved successfully!"
                ntf2.send()
                save_event.clear()
                stop_event.set()
            time.sleep(0.1)
        listener.stop()

    browser.close()
    time.sleep(1)
    exit()

# Load cookies and access messages
cookies = pickle.load(open(COOKIES_FILE, "rb"))
context.add_cookies(cookies)

page.reload()
time.sleep(1)
page.goto("https://www.tiktok.com/messages?lang=pt-BR")

page.wait_for_selector('[data-e2e="chat-list-item"]')

# Use all messages
WORDS = ["desenrolado", "orea seca", "fogo", "sossegado", "feijao com farinha", "moleculas aahh"]
conversation_items = page.query_selector_all('[data-e2e="chat-list-item"]')
total = len(conversation_items)
print(f"{total} conversations found.")

for i in range(total):
    try:
        conversation_items = page.query_selector_all('[data-e2e="chat-list-item"]')
        conversation_items[i].click()
        print(f"[{i+1}/{total}] Conversation(s) opened.")

        page.wait_for_selector('[data-e2e="message-input-area"] [contenteditable="true"]')
        boxx = page.locator('[data-e2e="message-input-area"] [contenteditable="true"]')
        boxx.click()
        time.sleep(1)

        msg = random.choice(WORDS)
        page.keyboard.type(msg, delay=200)

        time.sleep(0.5)
        page.keyboard.press("Enter")
        print(f"[{i+1}/{total}] Sent: '{msg}'")
        time.sleep(2)

    except Exception as e:
        print(f"[{i+1}/{total}] Erro: {e}")
        continue

# Register and close
T_FILE.write_text(str(today.day), encoding="utf-8")

print("All messages sent.")
browser.close()