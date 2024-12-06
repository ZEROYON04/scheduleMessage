from sendMessage import wrapped_send_text_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import json
import time
from logging import getLogger, config
from scheduleManager import display_scheduled_messages

with open("./log_config.json", "r") as f:
    log_conf = json.load(f)
config.dictConfig(log_conf)
logger = getLogger(__name__)


def main():
    with open("./schedule.json", "r") as file:
        data = json.load(file)
        email = data["email"]
        password = data["password"]
        defaultRoom = data["defaultRoom"]
    print(f"email: {email}, defaultRoom: {defaultRoom}")
    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    wrapped_send_text_message(
        email, password, "Message scheduler started!!", defaultRoom
    )
    # Add one-time schedules
    for one_time_schedule in data.get("oneTimeSchedules", []):
        run_date = datetime(
            one_time_schedule["year"],
            one_time_schedule["month"],
            one_time_schedule["day"],
            one_time_schedule["hour"],
            one_time_schedule["minute"],
        )
        room = one_time_schedule.get("room", defaultRoom)
        text = one_time_schedule.get("message", "Default message")
        scheduler.add_job(
            func=wrapped_send_text_message,
            args=[email, password, text, room],
            trigger="date",
            run_date=run_date,
        )
    logger.info("One-time schedules loaded.")
    # Add weekly schedules
    for schedule in data.get("weeklySchedules", []):
        day_of_week = schedule["dayOfWeek"]
        hour = schedule["hour"]
        minute = schedule["minute"]
        room = schedule.get("room", defaultRoom)
        text = schedule.get("message", "Error: No message provided.")
        scheduler.add_job(
            func=wrapped_send_text_message,
            args=[email, password, text, room],
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
        )
    logger.info("Weekly schedules loaded.")

    # Start the scheduler
    scheduler.start()
    display_scheduled_messages(data)
    logger.info("Scheduler started.")
    print("Scheduler started.Press Ctrl+C to stop.")
    # Wait to prevent the main thread from exiting
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()
