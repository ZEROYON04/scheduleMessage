from sendMessage import wrapped_send_text_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import json
from logging import getLogger, config

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
    logger.info(f"email: {email}, defaultRoom: {defaultRoom}")
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
        print(
            f"One-time Schedule - Run Date: {run_date}, Room: {room}, Message: {text}"
        )
        scheduler.add_job(
            func=wrapped_send_text_message,
            args=[email, password, text, room],
            trigger="date",
            run_date=run_date,
        )
    # Add weekly schedules
    for schedule in data.get("weeklySchedules", []):
        day_of_week = schedule["dayOfWeek"]
        hour = schedule["hour"]
        minute = schedule["minute"]
        room = schedule.get("room", defaultRoom)
        text = schedule.get("message", "Error: No message provided.")
        logger.info(
            f"Day: {day_of_week}, Time: {hour}:{minute}, Room: {room}, Message: {text}"
        )

        scheduler.add_job(
            func=wrapped_send_text_message,
            args=[email, password, text, room],
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
        )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started.Press Ctrl+C to stop.")
    # Wait to prevent the main thread from exiting
    try:  # Show menu and handle user input
        while True:
            print("\nMenu:")
            print("1. View current tasks")
            print("2. Add new one-time message")
            print("Press Ctrl+C to exit.")
            choice = input("Enter your choice: ")

            if choice == "1":
                jobs = scheduler.get_jobs()
                if not jobs:
                    print("No scheduled tasks.\n")
                else:
                    for job in jobs:
                        if callable(job.func):
                            print(
                                f"\nMessage: {job.args[2]}, Room:{job.args[3]},  Next Run Time: {job.next_run_time}"
                            )  # Potential bug due to arguments being specified by order
            elif choice == "2":
                try:
                    text = input("Enter text message: ")
                    room = input("Enter room: ")
                    while True:
                        run_date_str = input("Enter run date (YYYY-MM-DD HH:MM:SS): ")
                        try:
                            run_date = datetime.strptime(
                                run_date_str, "%Y-%m-%d %H:%M:%S"
                            )
                            break
                        except ValueError:
                            print(
                                "Incorrect format. Please enter the date in the format YYYY-MM-DD HH:MM:SS."
                            )

                    confirm = input("Do you want to schedule this task? (y/n): ")
                    if confirm.lower() == "y":
                        scheduler.add_job(
                            func=wrapped_send_text_message,
                            args=[email, password, text, room],
                            trigger="date",
                            run_date=run_date,
                        )
                        print("Task scheduled.\n")
                        logger.info(
                            f"Task scheduled - Message: {text}, Room: {room}, Run Date: {run_date}"
                        )
                    else:
                        print("Task not scheduled.\n")
                except KeyboardInterrupt:
                    print("Task not scheduled.\n")
            else:
                print("Invalid choice. Please try again.\n")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
