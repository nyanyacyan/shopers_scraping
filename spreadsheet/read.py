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

from logger.debug_logger import Logger

load_dotenv()

class SpreadsheetRead:
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

    
    def spreadsheet_read(self):
        '''
        JANと商品名をスプシから読み取る=> 組み合わせる=> 検索ワードに変換
        '''
        first_worksheet = self.gs.open_by_key(self.spreadsheet_key).worksheet("リサーチ情報入力")

        jan_data = first_worksheet.col_values(2)[1:]  # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        self.logger.debug(jan_data)

        item_name_data = first_worksheet.col_values(3)[1:]  # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        self.logger.debug(item_name_data)

        # JANと商品名をリスト内包表記へ
        mixdata = {jan: name for jan, name in zip(jan_data, item_name_data)}
        self.logger.debug(mixdata)

        return mixdata



