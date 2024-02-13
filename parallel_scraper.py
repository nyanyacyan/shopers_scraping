# ----------------------------------------------------------------------------------
# 非同期処理 scraper　並列処理クラス
# 2023/2/13制作

# ----------------------------------------------------------------------------------
import asyncio
import os

# 自作モジュール
from logger.debug_logger import Logger
from scraper.scraper_subclass.cookie import ScraperNetsea, ScraperOroshiuri, ScraperPetpochitto, ScraperTajimaya

class ParallelScraper:
    def __init__(self):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # インスタンス生成
        self.netsea_instance = ScraperNetsea(debug_mode=True)
        self.oroshiuri_instance = ScraperOroshiuri(debug_mode=True)
        self.petpochitto_instance = ScraperPetpochitto(debug_mode=True)
        self.tajimaya_instance = ScraperTajimaya(debug_mode=True)

    # それぞれのタスクに対して例外処理を実施
    async def scraper_wrapper(self, scraper_method, search_word):
        try:
            await scraper_method(search_word)
        except Exception as e:
            self.logger.error(f"処理中にエラーが発生しました: {e}")

    # それぞれのタスクを並列処理
    async def parallel_scraper(self, search_word):
        # ここに処理するものを追加していく
        results = await asyncio.gather(
            self.scraper_wrapper(self.netsea_instance.scraper_netsea_async, search_word),
            self.scraper_wrapper(self.oroshiuri_instance.scraper_oroshiuri_async, search_word),
            self.scraper_wrapper(self.petpochitto_instance.scraper_petpochitto_async, search_word),
            self.scraper_wrapper(self.tajimaya_instance.scraper_tajimaya_async, search_word)
        )

        # スプシの順番に沿って、上から順番に辞書に入れ込む
        results_dict = {
            "netsea": results[0],
            "oroshiuri": results[1],
            "petpochitto": results[2],
            "tajimaya": results[3]
        }

        return results_dict

# if __name__ == "__main__":
#     pal = ParallelScraper()
#     search_word = '9784861488542 れんそうカード'
#     asyncio.run(pal.parallel_scraper(search_word))