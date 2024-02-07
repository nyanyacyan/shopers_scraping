# coding: utf-8
# ----------------------------------------------------------------------------------
# テスト スプシ読込とオートログインを同時に行う
# 2023/2/6制作
# ----------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

# 自作モジュール
from autologin.autologin_subclass.auto_login_netsea_async import AutoLoginNetsea
from scraper.scraper_subclass.scaper_netsea_async import ScraperNetsea
from logger.debug_logger import Logger

load_dotenv()

class AutoScraperNetsea:
    def __init__(self, debug_mode=False):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
        chrome_options.add_argument("--window-size=1680,1200")  # ウィンドウサイズの指定

        # ChromeDriverManagerを使用して自動的に適切なChromeDriverをダウンロードし、サービスを設定
        service = Service(ChromeDriverManager().install())

        # WebDriverインスタンスを生成
        self.chrome = webdriver.Chrome(service=service, options=chrome_options)

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


    async def auto_scraper_netsea_async(self):
        search_word = f"9784861488542 れんそうカード"  # 例としてあげてる=> 後で受けられるように変更必要

        # autologinインスタンス
        auto_login_netsea = AutoLoginNetsea(chrome=self.chrome, debug_mode=self.debug_mode)

        # scraperインスタンス
        scraper_netsea = ScraperNetsea(chrome=self.chrome, debug_mode=True)

        self.logger.info("netseaオートログイン開始")
        await auto_login_netsea.auto_login_netsea_async()
        self.logger.info("netseaオートログイン完了")



        self.logger.info("netseaスクレイピング開始")
        netsea_data = await scraper_netsea.scraper_netsea_async(search_word)
        self.logger.info(f"netseaスクレイピング終了:{netsea_data}")

        return netsea_data