import os
import asyncio

# 自作モジュール
from logger.debug_logger import Logger
from autologin.autologin_subclass.auto_login_subclass_cookie import AutoLoginNetsea, AutoLoginOroshiuri, AutoLoginPetpochitto, AutoLoginTajimaya

class ParallelAutoLogin:
    def __init__(self):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # インスタンス生成
        self.netsea_instance = AutoLoginNetsea(debug_mode=True)
        self.oroshiuri_instance = AutoLoginOroshiuri(debug_mode=True)
        self.petpochitto_instance = AutoLoginPetpochitto(debug_mode=True)
        self.tajimaya_instance = AutoLoginTajimaya(debug_mode=True)


    async def parallel_auto_login(self):
        self.logger.info("並行処理を開始")
        await asyncio.gather(
            self.netsea_instance.auto_login_netsea_async(),
            self.oroshiuri_instance.auto_login_oroshiuri_async(),
            self.petpochitto_instance.auto_login_petpochitto_async(),
            self.tajimaya_instance.auto_login_tajimaya_async()
        )
        self.logger.info("並行処理完了")

if __name__ == "__main__":
    pal = ParallelAutoLogin()
    asyncio.run(pal.parallel_auto_login())
