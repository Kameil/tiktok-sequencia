import os
import time
import pickle
import random
from datetime import datetime
from platform import system

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from notifypy import Notify
from pynput import keyboard

from config import get_paths_by_os, get_flags_by_os

today = datetime.now()
with open("t.txt", "r", encoding="utf-8") as file:
    if file.read() == str(today.day):
        print("Already sent today")
        time.sleep(5)
        exit()

should_exit = False
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
flags = get_flags_by_os(os_name)
for flag in flags:
    option.add_argument(flag)

option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

browser = webdriver.Chrome(options=option)

browser.get("https://tiktok.com/")

if not os.path.exists("cookies.pkl"):
    print("No account found. Please log in and press Ctrl+S to save your cookies.")
    ntf = Notify()
    ntf.title = "Login with your account"
    ntf.message = "It Was not possible to find any account. Please log in and save your cookies."
    ntf.send()
    time.sleep(1)

    def save_cookies():
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
        print("Saved cookies.")
        ntf = Notify()
        ntf.title = "Cookies saved"
        ntf.message = "Please make sure you are logged in."
        ntf.send()

    def on_press(key):
        if key == keyboard.Key.esc:
            return False

        if key == keyboard.KeyCode.from_char('s') and any(
                modifier in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]
                for modifier in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]):
            save_cookies()

    print("Press Esc to exit or Ctrl+S to save again.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    browser.quit()
    time.sleep(1)
    exit()

# JA ENTRADO
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)
browser.refresh()
time.sleep(1)
# ir para mensagens
browser.get("https://www.tiktok.com/messages?lang=pt-BR")
time.sleep(10)
# clicar no primeiro usuario
browser.find_element(By.XPATH, '//*[@id="more-acton-icon-0"]/div/div[1]/div').click()
time.sleep(2)
# clicar na caixa de texto
browser.find_element(By.CLASS_NAME, "DraftEditor-root").click()
time.sleep(1)

# enviar
palavras = ["desenrolado", "orea seca"]
for x in random.choice(palavras):
    x = str(x)
    x = x.replace(" ", "space")
    keyboard.press(x)
    time.sleep(0.2)
time.sleep(0.5)
keyboard.press("enter")
with open("t.txt", "w", encoding="utf-8") as file:
     file.write(str(today.day))

# ntf = Notification(app_id="tiktok sequencia", title="Sequencia enviada")
# ntf.show()

time.sleep(2)
browser.quit()
