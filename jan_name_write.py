# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# jan,name スプレッドシート書込　　クラス
# 2023/2/13　制作

# ---------------------------------------------------------------------------------------------------------
import gspread
from google.auth.exceptions import RefreshError
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

from logger.debug_logger import Logger

load_dotenv()

class SpreadsheetWrite:
    def __init__(self, search_word,debug_mode=False):
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

        self.search_word = search_word
        


    def spreadsheet_write(self):
        # それぞれのワークシートを定義
        worksheet = self.gs.open_by_key(self.spreadsheet_key).worksheet("リサーチツール")

        # ２（B列）に書かれてる最後の行のセルに書かれてる内容
        last_cell_data = worksheet.col_values(2)
        self.logger.debug(last_cell_data)

        # 最初の空白
        first_blank_cell = len(last_cell_data) + 1
        self.logger.debug(first_blank_cell)

        # C列から順番に追記していく
        self.logger.debug("全サイトデータをスプシに書き込み開始")
        start_col = 3  # E列は「５」
        for jan, name in self.search_word.items():
            current_col = start_col
            try:
                worksheet.update_cell(first_blank_cell, current_col, jan)

                current_col += 1

                worksheet.update_cell(first_blank_cell, current_col, name)

            except gspread.exceptions.APIError as e:
                self.logger.error(f"APIエラーが発生しました: {e}")
            except RefreshError as e:
                self.logger.error(f"認証トークンの更新に失敗しました: {e}")
            except HttpError as e:
                self.logger.error(f"HTTPエラーが発生しました: {e}")


        self.logger.info("[jan][name]をスプシに書き込み完了")

if __name__ == "__main__":
    # テスト用の検索ワード辞書
    search_words = {
        "1234567890": "テスト商品1",
        "0987654321": "テスト商品2",
    }
    
    # SpreadsheetWriteクラスのインスタンスを作成
    spreadsheet_writer = SpreadsheetWrite(search_words)
    
    # スプレッドシートにデータを書き込む
    spreadsheet_writer.spreadsheet_write()