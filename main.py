import os
import time
import pickle
import random
from datetime import datetime
from platform import system
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from notifypy import Notify
from pynput import keyboard
from config import get_paths_by_os, get_flags_by_os

# Verify if it is already sent
today = datetime.now()
with open("t.txt", "r", encoding="utf-8") as file:
    if file.read() == str(today.day):
        print("Already sent today.")
        time.sleep(5)
        exit()

# Configure Chrome
option = Options()
chrome_paths = get_paths_by_os()
chrome_path = None

for name, path in chrome_paths.items():
    if os.path.exists(path):
        chrome_path = path
        print(f"Chrome found: {name} -> {path}")
        break

if not chrome_path:
    print("Error: No Chrome installation found!")
    exit(1)

option.binary_location = chrome_path
os_name = system()

for flag in get_flags_by_os(os_name):
    option.add_argument(flag)

option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# Initialize browser
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser, 10)
browser.get("https://tiktok.com/")

# Save cookies if not found
if not os.path.exists("cookies.pkl"):
    print("No account found. Please log in and press Ctrl+S to save your cookies.")

    ntf = Notify()
    ntf.title = "Login with your account"
    ntf.message = "No account found. Please log in and save your cookies."
    ntf.send()

    pressed_keys = set()

    def save_cookies():
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
        print("Cookies saved.")
        ntf = Notify()
        ntf.title = "Cookies saved"
        ntf.message = "Cookies saved successfully!"
        ntf.send()

    def on_press(key):
        pressed_keys.add(key)
        ctrl_held = {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r} & pressed_keys
        if key == keyboard.KeyCode.from_char('s') and ctrl_held:
            save_cookies()

    def on_release(key):
        pressed_keys.discard(key)
        if key == keyboard.Key.esc:
            return False

    print("Press Esc to exit or Ctrl+S to save cookies.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    browser.quit()
    time.sleep(1)
    exit()

# Load cookies and access messages
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

browser.refresh()
time.sleep(1)
browser.get("https://www.tiktok.com/messages?lang=pt-BR")

wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '[data-e2e="chat-list-item"]')
))

# Use all messages
WORDS = ["desenrolado", "orea seca", "fogo", "sossegado", "feijao com farinha", "moleculas aahh"]
conversation = browser.find_elements(By.CSS_SELECTOR, '[data-e2e="chat-list-item"]')
total = len(conversation)
print(f"{total} conversations found.")

for i in range(total):
    try:
        conversation = browser.find_elements(By.CSS_SELECTOR, '[data-e2e="chat-list-item"]')
        conversation[i].click()
        print(f"[{i+1}/{total}] Conversation(s) opened.")

        boxx = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-e2e="message-input-area"] [contenteditable="true"]')
        ))
        boxx.click()
        time.sleep(1)

        msg = random.choice(WORDS)
        for char in msg:
            key = "space" if char == " " else char
            keyboard.press(key)
            time.sleep(0.2)

        time.sleep(0.5)
        keyboard.press("enter")
        print(f"[{i+1}/{total}] Sent: '{msg}'")
        time.sleep(2)

    except Exception as e:
        print(f"[{i+1}/{total}] Erro: {e}")
        continue

# Register and close
with open("t.txt", "w", encoding="utf-8") as file:
    file.write(str(today.day))

print("All messages sent.")
browser.quit()