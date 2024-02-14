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
import asyncio
from functools import partial

from logger.debug_logger import Logger

load_dotenv()

class PriceUrlSpreadsheetWrite:
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
        


    def price_url_spreadsheet_write(self):
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

        self.logger.debug(self.results_dict)
        start_col = 5  # E列は「５」


        # 辞書の各要素をサイト別に置換して「価格」と「url」を抽出してスプシに反映
        for index,(site, info) in enumerate(self.results_dict.items()):
            current_col = start_col + index

            try:
                price = info['price']
                url = info['url']

                self.logger.debug(f"データ確認 {price},{url}")

                # urlがない場合は価格（該当なし）のみを表記する
                if url:
                    hyperling_formula = f'=HYPERLINK("{url}", "{price}")'
                    worksheet.update_cell(first_blank_cell, current_col, hyperling_formula)
                else:
                    worksheet.update_cell(first_blank_cell, current_col, str(price))

            except gspread.exceptions.APIError as e:
                self.logger.error(f"APIエラーが発生しました: {e}")
            except RefreshError as e:
                self.logger.error(f"認証トークンの更新に失敗しました: {e}")
            except HttpError as e:
                self.logger.error(f"HTTPエラーが発生しました: {e}")


        self.logger.debug("全サイトデータをスプシに書き込み完了")

        return True


    # 非同期化
    async def price_url_spreadsheet_write_async(self):
        loop = asyncio.get_running_loop()

        func = partial(self.price_url_spreadsheet_write)

        await loop.run_in_executor(None, func)
