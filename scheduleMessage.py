from sendMessage import wrapped_send_text_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import argparse
from datetime import datetime
import json

with open("./schedule.json", "r") as file:
    data = json.load(file)
    email = data["email"]
    password = data["password"]
    defaultRoom = data["defaultRoom"]


print(email, password, defaultRoom)
# スケジューラを初期化
scheduler = BackgroundScheduler()
timestamp = f"{datetime.now()}"
wrapped_send_text_message(email, password, "Message scheduler started!!", defaultRoom)


# スケジュールを表示


# スケジューラを開始
scheduler.start()

# メインスレッドを終了させないように待機
try:
    print("Scheduler started. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")
