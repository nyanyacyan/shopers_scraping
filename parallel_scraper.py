# ----------------------------------------------------------------------------------
# 非同期処理 scraper　並列処理クラス
# 2023/2/13制作

# ----------------------------------------------------------------------------------
import asyncio
import os

# 自作モジュール
from logger.debug_logger import Logger
from scraper.scraper_subclass.cookie import ScraperNetsea, ScraperOroshiuri, ScraperPetpochitto, ScraperTajimaya
from scraper.autologin_scraper_nocookie import SuperDeliveryAutologinScraper

class ParallelScraper:
    def __init__(self, search_word, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # インスタンス生成
        self.netsea_instance = ScraperNetsea(debug_mode=True)
        self.oroshiuri_instance = ScraperOroshiuri(debug_mode=True)
        self.petpochitto_instance = ScraperPetpochitto(debug_mode=True)
        self.super_delivery_instance = SuperDeliveryAutologinScraper(debug_mode=True)
        self.tajimaya_instance = ScraperTajimaya(debug_mode=True)

        self.search_word = search_word

    # それぞれのタスクに対して例外処理を実施
    async def scraper_wrapper(self, scraper_method, *args):
        try:
            result = await scraper_method(*args)
            return result
        except Exception as e:
            self.logger.error(f"処理中にエラーが発生しました: {e}")
            return None

    # それぞれのタスクを並列処理
    async def parallel_scraper(self, search_word):
        # ここに処理するものを追加していく

        netsea_task = asyncio.create_task(self.scraper_wrapper(self.netsea_instance.scraper_netsea_async, search_word)),
        oroshiuri_task = asyncio.create_task(self.scraper_wrapper(self.oroshiuri_instance.scraper_oroshiuri_async, search_word)),
        petpochitto_task = asyncio.create_task(self.scraper_wrapper(self.petpochitto_instance.
        scraper_petpochitto_async, search_word)),
        super_delivery_task = tajimaya_task = asyncio.create_task(self.scraper_wrapper(self.super_delivery_instance.super_delivery_async_cookieless_scraper, search_word)),
        tajimaya_task = asyncio.create_task(self.scraper_wrapper(self.tajimaya_instance.scraper_tajimaya_async, search_word))

        # スプシの順番に沿って、上から順番に辞書に入れ込む
        # データを追加する際にはここ入れていく
        await asyncio.gather(netsea_task, oroshiuri_task, petpochitto_task, super_delivery_task, tajimaya_task)

        results_dict = {
            "netsea": await netsea_task,
            "oroshiuri": await oroshiuri_task,
            "petpochitto": await petpochitto_task,
            "super_delivery": await super_delivery_task,
            "tajimaya": await tajimaya_task
        }

        self.logger.info(results_dict)
        return results_dict

if __name__ == "__main__":
    search_word = '9784861488542 れんそうカード'
    pal = ParallelScraper(search_word=search_word)
    asyncio.run(pal.parallel_scraper(search_word))