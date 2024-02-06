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
from scraper.scraper_subclass.scaper_netsea_async import ScraperNetsea
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

    # スプシ読込インスタンス
    spreadsheet_read = SpreadsheetRead(debug_mode=True)
    spreadsheet_read_async = SpreadsheetReadAsync(spreadsheet_read_instance=spreadsheet_read)  # 非同期

    # オートログインインスタンス
    auto_login_netsea = AutoLoginNetsea(chrome=chrome, debug_mode=True)

    # scraperインスタンス
    scraper_netsea = ScraperNetsea(chrome=chrome, debug_mode=True)

    start_time = time.time()
    print(f"処理開始: {time.ctime(start_time)}")


    # スプレッドシートの読み込みと自動ログインを並行して実行
    dic_data = await spreadsheet_read_async.spreadsheet_read_async()
    await auto_login_netsea.auto_login_netsea_async()

    for index, (jan, name) in enumerate(dic_data.items()):
        search_word = f"{jan} {name}"
        print(f"{index + 1}: {search_word}")

        await scraper_netsea.scraper_netsea(search_word)

    end_time = time.time()
    print(f"処理終了: {time.ctime(end_time)}")
    print(f"全体の処理時間: {end_time - start_time}秒")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())