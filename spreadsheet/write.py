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
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import datetime

from logger.debug_logger import Logger

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

        self.spreadsheet_key = os.getenv('SPREADSHEET_SITE_URL')
        

    def spreadsheet_write(self):
        # それぞれのワークシートを定義
        first_worksheet = self.gs.open_by_key(self.spreadsheet_key).worksheet("リサーチツール")

        # 現在の日付を YYYY-MM-DD 形式で取得
        current_date = datetime.datetime.now().strftime('%Y/%m/%d')

        last_cell_data = first_worksheet.col_values(2)  # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        self.logger.debug(last_cell_data)

        last_writed_cell = len(last_cell_data) + 1
        self.logger.debug(last_writed_cell)

# ここにスクレイピングしたデータを入れる
# すでに同じものがあった場合はエラーを出す=> その商品は飛ばすようにする
# ---------------------------------------------------------------------------------------------------------

        # スプシを更新
        # 列と行の指定が必要（last_writed_cell＝行,　２＝B列）

        # 日付の入力
        first_worksheet.update_cell(last_writed_cell, 2, current_date)

        # 画像
        # first_worksheet.update_cell(last_writed_cell, 3, current_date)

        # JAN
        # first_worksheet.update_cell(last_writed_cell, 4, 'データ')

        # 商品名
        # first_worksheet.update_cell(last_writed_cell, 5, 'データ')

        # 価格
        # first_worksheet.update_cell(last_writed_cell, 6, 'データ')

        # URL
        # first_worksheet.update_cell(last_writed_cell, 7, 'データ')


        





