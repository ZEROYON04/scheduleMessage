import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json


def main():
    with open("./schedule.json", "r") as file:
        data = json.load(file)
    email = data["email"]
    password = data["password"]
    defaultRoom = data["defaultRoom"]
    print(email, password, defaultRoom)

    # 現在時刻を取得
    current_time = datetime.now()

    sendText = f"現在の時刻は\n {current_time} \nです。"

    asyncio.run(
        send_text_message(
            email,
            password,
            sendText,
            defaultRoom,
        )
    )


async def send_text_message(email, password, sendText, room):
    """
    Sends a text message to a specified chat room using a browser automation tool.

    Args:
        email (str): The email address used for authentication.
        password (str): The password used for line authentication.
        sendText (str): The text message to be sent.
        room (str): The name of the chat room to send the message to.

    Raises:
        Exception: If an error occurs during the process, it will be caught and printed.

    Notes:
        This function uses Playwright for browser automation and requires the LINE
        browser extension to be installed and accessible at the specified path.
    """
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
        page = await browser.new_page()

        # 拡張機能のページにアクセス
        await page.goto(
            "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html",
        )
        print("拡張機能へアクセス")

        try:
            await page.wait_for_selector(
                ':is(input[name="password"], input.searchInput-module__input__ekGp7)'
            )
            # パスワードの入力と送信（必要であれば）
            if await page.is_visible(
                'input[name="password"]'
            ) and await page.is_visible('button[type="submit"]'):
                await page.fill('input[name="email"]', email)
                await page.fill('input[name="password"]', password)
                await page.click('button[type="submit"]')
                print("認証を実行")

            await page.wait_for_selector(
                ":is(strong.pinCodeModal-module__pincode__bFKMn, input.searchInput-module__input__ekGp7)"
            )
            if await page.is_visible("strong.pinCodeModal-module__pincode__bFKMn"):
                # strong要素内のテキストを取得
                pin_code = await page.text_content(
                    "strong.pinCodeModal-module__pincode__bFKMn"
                )
                # コンソールに出力
                print(f"取得したピンコード: {pin_code}")

            # ルームの検索
            await page.fill("input.searchInput-module__input__ekGp7", room)
            print("ルーム検索")
            await page.wait_for_selector('button[aria-label="Go chatroom"]')
            for _ in range(10):
                await page.click('button[aria-label="Go chatroom"]')
                if await page.is_visible("textarea.input"):
                    continue

            # メッセージの入力
            await page.fill("textarea.input", sendText)
            print("メッセージ入力")
            await page.keyboard.press("Enter")

            # 追加の待機が必要であれば非同期で待機
            await page.wait_for_timeout(1000)

        except Exception as e:
            print(f"エラーが発生しました: {e}")

        finally:
            # ブラウザを閉じる
            await browser.close()


def wrapped_send_text_message(email, password, sendText, room):
    """
    Sends a text message to a specified room using the provided email and password.

    This function wraps the asynchronous `send_text_message` function and runs it
    synchronously using `asyncio.run`.

    Args:
        email (str): The email address used for authentication.
        password (str): The password used for authentication.
        sendText (str): The text message to be sent.
        room (str): The identifier of the room where the message will be sent.

    Returns:
        None
    """
    asyncio.run(send_text_message(email, password, sendText, room))


if __name__ == "__main__":
    main()
