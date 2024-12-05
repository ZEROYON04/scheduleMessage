from sendMessage import wrapped_send_text_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
from datetime import datetime
import json
from logging import getLogger, config

with open("./log_config.json", "r") as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)

with open("./schedule.json", "r") as file:
    data = json.load(file)
    email = data["email"]
    password = data["password"]
    defaultRoom = data["defaultRoom"]


logger.info(f"email: {email}, password: {password}, defaultRoom: {defaultRoom}")
# スケジューラを初期化
scheduler = BackgroundScheduler()
timestamp = f"{datetime.now()}"
wrapped_send_text_message(email, password, "Message scheduler started!!", defaultRoom)


# スケジュールを表示
for schedule in data["schedules"]:
    dayOfWeek = schedule["day_of_week"]
    hour = schedule["hour"]
    minute = schedule["minute"]
    room = schedule["room"]
    text = schedule["message"]
    logger.info(f"Schedule: {dayOfWeek} {hour}:{minute} {room} {text}")

    scheduler.add_job(
        wrapped_send_text_message,
        args=[email, password, text, room],
        trigger=CronTrigger(day_of_week=dayOfWeek, hour=hour, minute=minute),
    )

# スケジューラを開始
scheduler.start()

# メインスレッドを終了させないように待機
try:
    logger.info("Scheduler started.Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logger.info("Scheduler stopped.")
