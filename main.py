import os
import time
import pickle
import random
from datetime import datetime
from notifypy import Notify
from pynput import keyboard as pynput_keyboard
from cloakbrowser import launch

# Verify if it is already sent
today = datetime.now()
with open("t.txt", "r", encoding="utf-8") as file:
    if file.read() == str(today.day):
        print("Already sent today.")
        time.sleep(5)
        exit()

# Initialize browser
browser = launch(headless=False, args=["--ozone-platform=x11"])
context = browser.new_context()
page = context.new_page()
page.goto("https://tiktok.com/")

# Save cookies if not found
if not os.path.exists("cookies.pkl"):
    print("No account found. Please log in and press Ctrl+S to save your cookies.")

    ntf = Notify()
    ntf.title = "Login with your account"
    ntf.message = "No account found. Please log in and save your cookies."
    ntf.send()

    pressed_keys = set()

    def save_cookies():
        cookies = context.cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))
        print("Cookies saved.")
        ntf = Notify()
        ntf.title = "Cookies saved"
        ntf.message = "Cookies saved successfully!"
        ntf.send()

    def on_press(key):
        pressed_keys.add(key)
        ctrl_held = {pynput_keyboard.Key.ctrl_l, pynput_keyboard.Key.ctrl_r} & pressed_keys
        if key == pynput_keyboard.KeyCode.from_char('s') and ctrl_held:
            save_cookies()

    def on_release(key):
        pressed_keys.discard(key)
        if key == pynput_keyboard.Key.esc:
            return False

    print("Press Esc to exit or Ctrl+S to save cookies.")
    with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    browser.close()
    time.sleep(1)
    exit()

# Load cookies and access messages
cookies = pickle.load(open("cookies.pkl", "rb"))
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
with open("t.txt", "w", encoding="utf-8") as file:
    file.write(str(today.day))

print("All messages sent.")
browser.close()