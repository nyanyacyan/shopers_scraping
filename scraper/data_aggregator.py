# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# 非同期処理　クラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
import datetime
from autologin import AutoLoginNetsea, AutoLoginOroshiuri, AutoLoginPetpochitto, AutoLoginSuperDelivery, AutoLoginTajimaya
from scraper import ScraperNetsea, ScraperOroshiuri, ScraperPetpochitto, ScraperSuperDelivery, ScraperTajimaya

from spreadsheet.read import SpreadsheetRead

from spreadsheet import SpreadsheetWriteNetsea #, SpreadsheetWriteOroshiuri, SpreadsheetWritePetpochitto, SpreadsheetWriteSuperDelivery, SpreadsheetWriteTajimaya

from logger.debug_logger import Logger

load_dotenv()

class DataAggregator:
    def __init__(self, chrome, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        self.chrome = chrome

        # スプシに書き込むデータを集約する箱
        self.scraped_data = {}

        # netseaインスタンス生成
        self.netsea_spreadsheet_read_instance = SpreadsheetRead(self.chrome)
        self.netsea_auto_login_instance = AutoLoginNetsea(self.chrome)
        self.netsea_scraper_instance = ScraperNetsea(self.chrome)
        self.netsea_spreadsheet_write_instance = SpreadsheetWriteNetsea(self.chrome)

    # スプシからのデータを受けてNETSEAのオートログインからスクレイピングして価格とURLを入手して共通の箱に入れる
    def data_aggregate(self):
        dic_data = self.spreadsheet_read_instance.spreadsheet_read()
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.logger.debug(f"スプシ記載されたJAN、商品名: {dic_data}")

        for index, (jan, name) in enumerate(dic_data.items()):
            search_word = f"{jan} {name}"
            self.logger.debug(f"{index + 1}: {search_word}")

            if jan not in self.scraped_data:  # 同じJANがない場合のみ入れ込む
                self.scraped_data[jan] = {
                    "date": current_date,
                    "jan": jan,
                    "name": name,
                    "sites": {}
                }
            else:
                # 同じJANコードが選定されていた場合にスキップ
                self.logger.info("商品（JAN）が選定されてます。この商品はスキップします")
                continue

            self.scraped_data[jan]["sites"]["netsea"] = {
                "price": "メソッドで呼び出す",
                "url": "メソッドで呼び出す"
            }




