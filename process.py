# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# 非同期処理　クラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
import asyncio

from autologin import AutoLoginNetsea, AutoLoginOroshiuri, AutoLoginPetpochitto, AutoLoginSuperDelivery, AutoLoginTajimaya
from scraper import ScraperNetsea, ScraperPetpochitto, ScraperSuperDelivery, ScraperTajimaya
from scraper.scraper_subclass.scraper_oroshiuri import ScraperOroshiuri

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

        self.spreadsheet_read_instance = SpreadsheetRead(self.chrome)

        # netseaインスタンス生成
        self.auto_login_netsea_instance = AutoLoginNetsea(self.chrome)
        self.scraper_netsea_instance = ScraperNetsea(self.chrome)

        # oroshiuriインスタンス生成
        self.auto_login_oroshiuri_instance = AutoLoginOroshiuri(self.chrome)
        self.scraper_oroshiuri_instance = ScraperOroshiuri(self.chrome)


    def process_scraper_netsea(self):
        dic_data = self.spreadsheet_read_instance.spreadsheet_read()
        self.logger.debug(f"スプシ記載されたJAN、商品名: {dic_data}")

        for index, (jan, name) in enumerate(dic_data.items()):
            search_word = f"{jan} {name}"
            self.logger.debug(f"{index + 1}: {search_word}")



            self.logger.debug("netseaオートログイン開始")
            self.auto_login_netsea_instance.auto_login_netsea()
            self.logger.debug("netseaオートログイン完了")

            self.logger.debug("netseaスクレイピング開始")
            self.chrome.save_screenshot("before{index}.png")
            self.scraper_netsea_instance.scraper_netsea(search_word)
            self.logger.debug("netseaスクレイピング終了")


    def process_scraper_oroshiuri(self):
        dic_data = self.spreadsheet_read_instance.spreadsheet_read()
        self.logger.debug(f"スプシ記載されたJAN、商品名: {dic_data}")

        self.logger.debug("oroshiuriオートログイン開始")
        self.auto_login_oroshiuri_instance.auto_login_oroshiuri()
        self.logger.debug("oroshiuriオートログイン完了")

        

        for index, (jan, name) in enumerate(dic_data.items()):
            search_word = f"{jan} {name}"
            self.logger.debug(f"{index + 1}: {search_word}")
            
            self.logger.debug("oroshiuriスクレイピング開始")
            self.scraper_oroshiuri_instance.scraper_oroshiuri(search_word)
            self.logger.debug("oroshiuriスクレイピング終了")
