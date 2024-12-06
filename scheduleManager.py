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

    print(f"email: {email}, defaultRoom: {defaultRoom}")
    while True:
        print("\nMenu:")
        print("1. View current scheduled messages")
        print("2. Add new one-time message")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            display_scheduled_messages(data)
        elif choice == "2":
            schedule_one_time_message()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")


def display_scheduled_messages(data):
    for one_time_schedule in data.get("oneTimeSchedules", []):
        run_date = datetime(
            one_time_schedule["year"],
            one_time_schedule["month"],
            one_time_schedule["day"],
            one_time_schedule["hour"],
            one_time_schedule["minute"],
        )
        room = one_time_schedule["room"]
        text = one_time_schedule.get("message", "Default message")
        print(f"Run Date: {run_date}, Room: {room}, Message: {text}")

    for schedule in data.get("weeklySchedules", []):
        day_of_week = schedule["dayOfWeek"]
        hour = schedule["hour"]
        minute = schedule["minute"]
        room = one_time_schedule["room"]
        text = schedule.get("message", "Error: No message provided.")
        print(
            f"Day of Week: {day_of_week}, Time: {hour}:{minute}, Room: {room}, Message: {text}"
        )


def schedule_one_time_message():
    try:
        text = input("Enter text message: ")
        room = input("Enter room: ")
        while True:
            run_date_str = input("Enter run date (MM-DD HH:MM): ")
            try:
                current_year = datetime.now().year
                run_date = datetime.strptime(
                    f"{current_year}-{run_date_str}", "%Y-%m-%d %H:%M"
                )
                if run_date < datetime.now():
                    run_date = run_date.replace(year=current_year + 1)
                break
            except ValueError:
                print(
                    "Incorrect format. Please enter the date in the format MM-DD HH:MM."
                )

        confirm = input("Do you want to schedule this task? (y/n): ")
        if confirm.lower() == "y":
            # Add the task to schedule.json
            new_task = {
                "year": run_date.year,
                "month": run_date.month,
                "day": run_date.day,
                "hour": run_date.hour,
                "minute": run_date.minute,
                "room": room,
                "message": text,
            }

            # Read schedule.json
            with open("./schedule.json", "r") as file:
                data = json.load(file)

            data["oneTimeSchedules"].append(new_task)

            # Rewrite schedule.json
            with open("./schedule.json", "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            logger.info("Task added to schedule.json.")

            print("Task scheduled.\n")
            logger.info(f"Task scheduled - Run Date: {run_date}")
        else:
            print("Task not scheduled.\n")
    except KeyboardInterrupt:
        print("Task not scheduled.\n")


if __name__ == "__main__":
    main()
