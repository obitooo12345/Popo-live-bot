import json
import time
import threading
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Configuration ===
ACCOUNTS_FILE = "accounts.json"
GECKO_PATH = "/data/data/com.termux/files/home/geckodriver"
MAX_RETRIES = 2

STREAM_SUCCESS_CHECK = {
    "by": By.ID,
    "value": "live-timer",
    # "url_contains": "/live-room"
}

LOGIN_URL = "https://www.popo.live/login"
GO_LIVE_URL = "https://www.popo.live/go-live"

# === Helpers ===
def load_accounts():
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def setup_driver():
    opts = Options()
    opts.headless = True
    service = Service(GECKO_PATH)
    driver = webdriver.Firefox(service=service, options=opts)
    driver.set_page_load_timeout(60)
    return driver

def wait_for(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# === Core Logic ===
def go_live(account):
    user, pwd = account["username"], account["password"]
    print(f"[{user}] Initiating stream...")
    driver = setup_driver()
    try:
        driver.get(LOGIN_URL)
        wait_for(driver, By.ID, "username").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(pwd)
        driver.find_element(By.CLASS_NAME, "login-btn").click()

        time.sleep(5)  # wait after login
        driver.get(GO_LIVE_URL)

        wait_for(driver, By.ID, "go-live-btn").click()
        time.sleep(5)

        ok = False
        try:
            wait_for(driver, STREAM_SUCCESS_CHECK["by"], STREAM_SUCCESS_CHECK["value"], timeout=15)
            ok = True
        except:
            pass

        if not ok and "url_contains" in STREAM_SUCCESS_CHECK:
            ok = STREAM_SUCCESS_CHECK["url_contains"] in driver.current_url

        if ok:
            print(f"[{user}] ✅ Stream live!")
            return True
        else:
            print(f"[{user}] ❌ Stream failed to start.")
            return False

    except Exception as e:
        print(f"[{user}] ❗ Error: {e}")
        return False
    finally:
        driver.quit()

def try_stream(account):
    user = account["username"]
    for attempt in range(1, MAX_RETRIES + 1):
        if go_live(account):
            return
        print(f"[{user}] Retrying... ({attempt}/{MAX_RETRIES})")
        time.sleep(10)
    print(f"[{user}] ⚠️ All retries failed after {MAX_RETRIES} attempts.")

def run_all_streams():
    accounts = load_accounts()
    for i, acc in enumerate(accounts):
        threading.Timer(i * 10, try_stream, args=[acc]).start()

# === Scheduler setup ===
schedule.every().day.at("03:00").do(run_all_streams)

print("Scheduler running: waiting for 03:00 daily...")
while True:
    schedule.run_pending()
    time.sleep(30)
