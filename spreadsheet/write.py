# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スプレッドシート書込　　親クラス
# 2023/1/30制作

#---バージョン---
# Python==3.8.10


#---流れ--
# 入力項目=> 日付=> 画像=> JAN=> 商品名=> 価格=> URL
# ---------------------------------------------------------------------------------------------------------
import gspread
from google.auth.exceptions import RefreshError
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
import datetime

from logger.debug_logger import Logger
from gather_site_data_async import GatherSiteDataAsync

load_dotenv()

class SpreadsheetWrite:
    def __init__(self, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        service_account_file = os.getenv('GCP_JSONFILE')

        credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scopes)

        self.gs = gspread.authorize(credentials)

        self.spreadsheet_key = os.getenv('SPREADSHEET_KEY')
        


    async def spreadsheet_write(self):
        # インスタンス化
        gatherer = GatherSiteDataAsync()
        # それぞれのワークシートを定義
        worksheet = self.gs.open_by_key(self.spreadsheet_key).worksheet("リサーチツール")

        # 集計データ読み込み
        sites_data = await gatherer.gather_site_data_async()
        self.logger.debug(sites_data)

        # 現在の日付を YYYY-MM-DD 形式で取得
        current_date = datetime.datetime.now().strftime('%Y/%m/%d')

        # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        last_cell_data = worksheet.col_values(2)
        self.logger.debug(last_cell_data)

        last_writed_cell = len(last_cell_data) + 1
        self.logger.debug(last_writed_cell)

        # 日付の挿入
        worksheet.update_cell(last_writed_cell, 2, current_date)

        # E列から順番に追記していく
        start_cell = 5  # E列は「５」
        for item in sites_data:
            hyperlink = f'=HYPERLINK("{item["url"]}", "{item["price"]}")'

            try:
                worksheet.update_cell(last_writed_cell, start_cell, hyperlink)
            except gspread.exceptions.APIError as e:
                self.logger.error(f"APIエラーが発生しました: {e}")
            except RefreshError as e:
                self.logger.error(f"認証トークンの更新に失敗しました: {e}")
            except HttpError as e:
                self.logger.error(f"HTTPエラーが発生しました: {e}")

            start_cell += 1
