# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スプレッドシート書込　　親クラス
# 2023/1/30制作

#---バージョン---
# Python==3.8.10


#---流れ--
# SpreadsheetReadクラスにてspreadsheet_readメソッドを設立=> 外部ライブラリのため非同期処理が必要
# => 非同期処理するためにSpreadsheetReadAsyncクラスを設立
# => spreadsheet_read_asyncメソッドにより非同期処理ができるようにspreadsheet_readメソッドの行なってる処理（asyncio.get_running_loop）を取得（実際のインスタンスを受け取って非同期処理ができるように加工するイメージ）
# 非同期処理は基本使わない方がいい→非同期処理は
# ---------------------------------------------------------------------------------------------------------
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import asyncio

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

        self.spreadsheet_key = os.getenv('SPREADSHEET_KEY')

    
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


class SpreadsheetReadAsync:
    def __init__(self, spreadsheet_read_instance):
        self.spreadsheet_read_instance = spreadsheet_read_instance

    
    async def spreadsheet_read_async(self):
        # 現在実行中のイベントループを取得　
        # イベントループとはスケジューラに近いもの。ここでのループという名前が示すものはプログラムが終了するまで処理を続けるって意味
        loop = asyncio.get_running_loop()

        # run_in_executorを使って同期的なspreadsheet_readメソッドを非同期で実行
        mixdata = await loop.run_in_executor(None, self.spreadsheet_read_instance.spreadsheet_read)

        return mixdata

