from sendMessage import wrapped_send_text_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="引数から値を取得するプログラム")

# 引数を定義（オプション引数）
parser.add_argument("--password", type=str, help="パスワード")
# 引数を解析
args = parser.parse_args()
# 引数が指定されていればその値を使用
if not args.password:
    print("引数 '--password' が指定されていません")


# スケジューラを初期化
scheduler = BackgroundScheduler()

# 毎週月曜日の20時にジョブを追加
scheduler.add_job(
    wrapped_send_text_message,
    args=[args.password, f"{datetime.now()}", "ぐる"],
    trigger=CronTrigger(day_of_week="wed", hour=22, minute=32),
)


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
