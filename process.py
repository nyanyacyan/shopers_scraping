from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import time

from autologin.autologin_subclass.auto_login_netsea import AutoLoginNetsea
from autologin.autologin_subclass.auto_login_oroshiuri import AutoLoginOroshiuri
from autologin.autologin_subclass.auto_login_petpochitto import AutoLoginPetpochitto
from autologin.autologin_subclass.auto_login_superdelivery import AutoLoginSuperDelivery
from autologin.autologin_subclass.auto_login_tajimaya import AutoLoginTajimaya

from scraper.scraper_subclass.scraper_netsea import ScraperNetsea
from scraper.scraper_subclass.scraper_oroshiuri import ScraperOroshiuri
from scraper.scraper_subclass.scraper_petpochitto import ScraperPetpochitto
from scraper.scraper_subclass.scraper_super_delivery import ScraperSuperDelivery
from scraper.scraper_subclass.scraper_tajimaya import ScraperTajimaya

from spreadsheet.read import SpreadsheetRead

from spreadsheet.write import SpreadsheetWrite

from logger.debug_logger import Logger

load_dotenv()

class Process:
    def __init__(self, chrome, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        self.chrome = chrome

        # インスタンス生成
        self.spreadsheet_read_instance = SpreadsheetRead(self.chrome)
        self.auto_login_instance = AutoLoginNetsea(self.chrome)
        self.scraper_instance = ScraperNetsea(self.chrome)
        # self.spreadsheet_write_instance = SpreadsheetWriteNetsea(self.chrome)


    def process_scraper_netsea(self):
        dic_data = self.spreadsheet_read_instance.spreadsheet_read()
        self.logger.debug(f"スプシ記載されたJAN、商品名: {dic_data}")

        for index, (jan, name) in enumerate(dic_data.items()):
            search_word = f"{jan} {name}"
            self.logger.debug(f"{index + 1}: {search_word}")

            self.logger.debug("netseaオートログイン開始")
            self.auto_login_instance.auto_login_netsea()
            self.logger.debug("netseaオートログイン完了")

            self.logger.debug("netseaスクレイピング開始")
            self.scraper_instance.scraper_netsea(search_word)
            self.logger.debug("netseaスクレイピング終了")

            # 書き込むデータごとに関数を呼び出す必要あり=> JAN、商品名、価格、画像、URL
            self.logger.debug("netseaデータをスプシに書込開始")
            self.spreadsheet_write_instance.write_netsea()
            self.logger.debug("netseaデータをスプシに書込終了")

