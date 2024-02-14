# ----------------------------------------------------------------------------------
# 非同期処理 Cookie保存　並列処理クラス
# 2023/2/13制作

# ----------------------------------------------------------------------------------
import asyncio
import os

# 自作モジュール
from logger.debug_logger import Logger
from jan_name_write import JanNameSpreadsheetWrite
from parallel_scraper import ParallelScraper
from spreadsheet.price_url_write import PriceUrlSpreadsheetWrite

class OneProduct:
    def __init__(self, search_word, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # インスタンス生成
        self.jan_name_spreadsheet_write = JanNameSpreadsheetWrite(debug_mode=True)
        self.parallel_scraper = ParallelScraper(search_word, debug_mode=True)
        

        self.search_word = search_word



    # それぞれのタスクに対して例外処理を実施
    async def one_product_wrapper(self, one_product_method, search_word, *args):
        try:
            return await one_product_method(search_word, *args)
        except Exception as e:
            self.logger.error(f"one_product_wrapperにて処理中にエラーが発生しました: {e}")
            return None

    # 同期処理
    async def one_product(self):
        await self.one_product_wrapper(self.jan_name_spreadsheet_write.jan_name_spreadsheet_write_async, self.search_word)
        results_dict = await self.one_product_wrapper(self.parallel_scraper.parallel_scraper, search_word=search_word)

        # results_dictの結果が出てからインスタンスの生成
        self.price_url_spreadsheet_write = PriceUrlSpreadsheetWrite(results_dict,debug_mode=True)
        self.logger.info(results_dict)

        try:
            self.logger.debug("price_url_spreadsheet_write開始")
            await self.price_url_spreadsheet_write.price_url_spreadsheet_write_async()
            self.logger.debug("price_url_spreadsheet_write終了")

        except Exception as e:
            self.logger.error(f"処理中にエラーが発生しました。{e}")

if __name__ == "__main__":
    search_word = '9784861488542 れんそうカード'

    one_product_instance = OneProduct(search_word=search_word, debug_mode=True)

    asyncio.run(one_product_instance.one_product())