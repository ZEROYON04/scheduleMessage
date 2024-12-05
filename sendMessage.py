import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
from logging import getLogger, config

with open("./log_config.json", "r") as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)
logger = getLogger(__name__)


def load_config(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def get_current_time_message():
    current_time = datetime.now()
    return f"現在の時刻は\n {current_time} \nです。"


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
        logger.info("拡張機能のページにアクセス")

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
                logger.info("ログイン")

            await page.wait_for_selector(
                ":is(strong.pinCodeModal-module__pincode__bFKMn, input.searchInput-module__input__ekGp7)"
            )
            if await page.is_visible("strong.pinCodeModal-module__pincode__bFKMn"):
                # strong要素内のテキストを取得
                pin_code = await page.text_content(
                    "strong.pinCodeModal-module__pincode__bFKMn"
                )
                # コンソールに出力
                logger.info(f"取得したピンコード: {pin_code}")

            # ルームの検索
            await page.fill("input.searchInput-module__input__ekGp7", room)
            logger.info("ルームの検索")
            await page.wait_for_selector('button[aria-label="Go chatroom"]')
            for _ in range(10):
                await page.click('button[aria-label="Go chatroom"]')
                if await page.is_visible("textarea.input"):
                    continue

            # メッセージの入力
            await page.fill("textarea.input", sendText)
            logger.info("メッセージの入力")
            await page.keyboard.press("Enter")

            # 追加の待機が必要であれば非同期で待機
            await page.wait_for_timeout(1000)

        except Exception as e:
            logger.error(e)

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


def main():
    config = load_config("./schedule.json")
    email = config["email"]
    password = config["password"]
    defaultRoom = config["defaultRoom"]
    logger.info(f"email: {email}, password: {password}, defaultRoom: {defaultRoom}")

    sendText = get_current_time_message()

    asyncio.run(
        send_text_message(
            email,
            password,
            sendText,
            defaultRoom,
        )
    )


if __name__ == "__main__":
    main()
