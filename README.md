# 🎥 Popo Live Auto-Streamer Bot

A Python bot that automatically logs into your Popo Live accounts and goes live at a scheduled time.  
Built for Termux or any Linux environment with Firefox and geckodriver.

---

## ✨ Features
- ✅ Automatically logs into multiple accounts
- ✅ Starts live streams at a set time
- ✅ Automatic retries if a stream fails
- ✅ Uses headless Firefox + Selenium
- ✅ Runs on Termux or any Linux server
- ✅ Staggered startup so accounts don’t overload the platform

---

## 🧰 Setup Instructions

### 1️⃣ Clone this repo
```bash
git clone https://github.com/YourUsername/popo-live-auto-streamer.git
cd popo-live-auto-streamer

2️⃣ Install dependencies

Make sure you have Python 3.x and geckodriver installed.

Then:

pip install selenium schedule

You can download geckodriver for Termux:

pkg install firefox
pkg install geckodriver

(Adjust GECKO_PATH in auto_stream.py if you install geckodriver somewhere else.)


---

3️⃣ Configure your accounts

Create an accounts.json file:

[
  {
    "username": "your_user_1",
    "password": "your_pass_1"
  },
  {
    "username": "your_user_2",
    "password": "your_pass_2"
  }
]

> ⚠️ Never commit this file.
A .gitignore file is already included.




---

4️⃣ Run the bot

Start the bot with:

python auto_stream.py
