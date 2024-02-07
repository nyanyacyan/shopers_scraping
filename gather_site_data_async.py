import asyncio
import os

from logger.debug_logger import Logger
from auto_scraper_oroshiuri import AutoScraperOroshiuri  # 自作クラスのインポートパスを適宜調整してください
from auto_scraper_netsea import AutoScraperNetsea

class GatherSiteDataAsync:
    def __init__(self, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

    async def gather_site_data_async(self):
        # 各クラスのインスタンスを作成
        netsea_scraper = AutoScraperNetsea(debug_mode=True)
        oroshiuri_scraper = AutoScraperOroshiuri(debug_mode=True)

        # 並列処理を実施して、それぞれの変数に代入
        self.logger.debug("並列処理開始")
        netsea_result, oroshiuri_result = await asyncio.gather(
            netsea_scraper.auto_scraper_netsea_async(),
            oroshiuri_scraper.auto_scraper_oroshiuri_async()
        )
        self.logger.debug("並列処理完了")

        # 各結果をresultsに追加
        results = []
        results.append(netsea_result)  # netsea_result をリストに追加
        results.append(oroshiuri_result) 

        # 結果を表示
        self.logger.debug(f"スクレイピング結果:{results}")

        return results