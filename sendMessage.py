from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import argparse


def main():

    # 現在時刻を取得
    current_time = datetime.now()

    # ArgumentParserを作成
    parser = argparse.ArgumentParser(description="引数から値を取得するプログラム")

    # 引数を定義（オプション引数）
    parser.add_argument("--password", type=str, help="パスワード")
    parser.add_argument("--room", type=str, help="グループ")

    # 引数を解析
    args = parser.parse_args()

    # 引数が指定されていればその値を使用
    if not args.password:
        print("引数 '--password' が指定されていません")
    if not args.room:
        print("引数 '--room' が指定されていません")

    sendText = (
        f"プログラムから送ってるから無視してね。現在の時刻は {current_time} です。"
    )

    send_text_message(
        args.password,
        sendText,
        args.room,
    )


def send_text_message(
    password,
    sendText,
    room,
):
    extension_path = "./3.6.0_0"  # 拡張機能のフォルダパス

    with sync_playwright() as p:
        # ブラウザを起動
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./save",  # ユーザーデータの保存先（空の場合、一時的に保存）
            headless=False,  # ヘッドレスモードでは拡張機能が動かない場合がある
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )

        # 新しいタブを開く
        page = browser.new_page()

        # 拡張機能のページにアクセス
        page.goto(
            "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html"
        )  # 拡張機能のページ

        # 必要な操作を記述
        if page.is_visible('input[name="password"]') and page.is_visible(
            'button[type="submit"]'
        ):
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
        page.fill("input.searchInput-module__input__ekGp7", room)
        page.wait_for_selector('button[aria-label="Go chatroom"]')
        page.click('button[aria-label="Go chatroom"]')
        page.fill("textarea.input", sendText)
        page.keyboard.press("Enter")
        time.sleep(1)
        # ブラウザを閉じる
        browser.close()


if __name__ == "__main__":
    main()
