# coding: utf-8
# ----------------------------------------------------------------------------------
# テスト スプシ読込とオートログインを同時に行う
# 2023/2/6制作
# ----------------------------------------------------------------------------------
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import functools
from dotenv import load_dotenv
import os
import time

# 自作モジュール
from autologin.autologin_subclass.auto_login_netsea_async import AutoLoginNetsea
from spreadsheet.read import SpreadsheetRead, SpreadsheetReadAsync
from logger.debug_logger import Logger

load_dotenv()

debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
logger_instance = Logger(__name__, debug_mode=debug_mode)
logger = logger_instance.get_logger()


async def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
    chrome_options.add_argument("--window-size=1680,1200")  # ウィンドウサイズの指定

    # ChromeDriverManagerを使用して自動的に適切なChromeDriverをダウンロードし、サービスを設定
    service = Service(ChromeDriverManager().install())

    # WebDriverインスタンスを生成
    chrome = webdriver.Chrome(service=service, options=chrome_options)

    spreadsheet_read = SpreadsheetRead(debug_mode=True)
    spreadsheet_read_async = SpreadsheetReadAsync(spreadsheet_read_instance=spreadsheet_read)

    auto_login_netsea = AutoLoginNetsea(chrome=chrome, debug_mode=True)

    start_time_spreadsheet = time.time()
    print(f"スプレッドシート読み込み開始: {time.ctime(start_time_spreadsheet)}")
    spreadsheet_data = await spreadsheet_read_async.spreadsheet_read_async()
    end_time_spreadsheet = time.time()

    start_time_login = time.time()
    print(f"自動ログイン処理開始: {time.ctime(start_time_login)}")
    await auto_login_netsea.auto_login_netsea_async()
    end_time_login = time.time()

    print(f"スプレッドシート読み込み時間: {end_time_spreadsheet - start_time_spreadsheet}秒")
    print(f"自動ログイン処理時間: {end_time_login - start_time_login}秒")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())