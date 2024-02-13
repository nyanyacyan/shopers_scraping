# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スプレッドシート書込　　親クラス
# 2023/2/13　制作

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

load_dotenv()

class SpreadsheetWrite:
    def __init__(self, results_dict,debug_mode=False):
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

        self.results_dict = results_dict
        


    def spreadsheet_write_async(self):
        # それぞれのワークシートを定義
        worksheet = self.gs.open_by_key(self.spreadsheet_key).worksheet("リサーチツール")

        # 現在の日付を YYYY-MM-DD 形式で取得
        current_date = datetime.datetime.now().strftime('%Y/%m/%d')

        # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        last_cell_data = worksheet.col_values(2)
        self.logger.debug(last_cell_data)

        # 最初の空白
        first_blank_cell = len(last_cell_data) + 1
        self.logger.debug(first_blank_cell)

        # 日付の挿入
        self.logger.debug("日付の挿入開始")
        worksheet.update_cell(first_blank_cell, 2, current_date)
        self.logger.debug("日付の挿入終了")

        # E列から順番に追記していく
        self.logger.debug("全サイトデータをスプシに書き込み開始")
        start_col = 5  # E列は「５」
        for site, data_list in self.results_dict.items():
            current_col = start_col

            try:
                for price, url in data_list:
                    hyperling_formula = f'=HYPERLINK("{url}", "{price}")'
                    worksheet.update_cell(first_blank_cell, current_col, hyperling_formula)
                    current_col += 1

            except gspread.exceptions.APIError as e:
                self.logger.error(f"APIエラーが発生しました: {e}")
            except RefreshError as e:
                self.logger.error(f"認証トークンの更新に失敗しました: {e}")
            except HttpError as e:
                self.logger.error(f"HTTPエラーが発生しました: {e}")


        self.logger.debug("全サイトデータをスプシに書き込み完了")
        first_blank_cell += 1  # 次の行へ