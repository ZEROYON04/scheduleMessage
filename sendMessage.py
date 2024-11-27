import asyncio
from playwright.async_api import async_playwright
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

    sendText = f"現在の時刻は {current_time} です。"

    asyncio.run(
        send_text_message(
            args.password,
            sendText,
            args.room,
        )
    )


async def send_text_message(password, sendText, room):
    extension_path = "./3.6.0_0"  # 拡張機能のフォルダパス

    async with async_playwright() as p:
        # ブラウザを起動
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./save",  # ユーザーデータの保存先（空の場合、一時的に保存）
            headless=False,  # ヘッドレスモードでは拡張機能が動かない場合がある
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )

        # 新しいタブを開く
        page = await browser.new_page()

        # 拡張機能のページにアクセス
        await page.goto(
            "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html"
        )  # 拡張機能のページ

        try:
            # パスワードの入力と送信（必要であれば）
            if await page.is_visible(
                'input[name="password"]'
            ) and await page.is_visible('button[type="submit"]'):
                await page.fill('input[name="password"]', password)
                await page.click('button[type="submit"]')

            # ルームの検索
            await page.fill("input.searchInput-module__input__ekGp7", room)
            await page.wait_for_selector('button[aria-label="Go chatroom"]')
            await page.click('button[aria-label="Go chatroom"]')

            # メッセージの入力
            await page.fill("textarea.input", sendText)
            await page.keyboard.press("Enter")

            # 追加の待機が必要であれば非同期で待機
            await page.wait_for_timeout(1000)

        except Exception as e:
            print(f"エラーが発生しました: {e}")

        finally:
            # ブラウザを閉じる
            await browser.close()


if __name__ == "__main__":
    main()
