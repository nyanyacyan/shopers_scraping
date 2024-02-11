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
from autologin.autologin_subclass.auto_login_subclass_cookie import AutoLoginSuperDelivery
from scraper.scraper_subclass.scaper_async_no_cookie_subclass import ScraperNocookieSuperDelivery
from logger.debug_logger import Logger

load_dotenv()

class AutoScrapersuper_delivery:
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


    async def cookieless_scraper_super_delivery_async(self, search_word):
        # autologinインスタンス
        auto_login_super_delivery = AutoLoginSuperDelivery(chrome=self.chrome, debug_mode=self.debug_mode)

        # scraperインスタンス
        scraper_super_delivery = ScraperNocookieSuperDelivery(chrome=self.chrome, debug_mode=True)

        self.logger.info("super_deliveryオートログイン開始")
        await auto_login_super_delivery.auto_login_super_delivery_async()
        self.logger.info("super_deliveryオートログイン完了")

        self.logger.info("super_deliveryスクレイピング開始")
        super_delivery_data = await scraper_super_delivery.scraper_super_delivery_async(search_word)
        self.logger.info(f"super_deliveryスクレイピング終了:{super_delivery_data}")

        return super_delivery_data