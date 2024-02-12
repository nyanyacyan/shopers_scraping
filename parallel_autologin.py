# ----------------------------------------------------------------------------------
# 非同期処理 Cookie保存　並列処理クラス
# 2023/2/9制作

#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
import asyncio
import os

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

    async def auto_login_wrapper(self, auto_login_method):
        try:
            await auto_login_method()
        except Exception as e:
            self.logger.error(f"処理中にエラーが発生しました: {e}")


    async def parallel_auto_login(self):
        await asyncio.gather(
            self.auto_login_method(self.netsea_instance.auto_login_netsea_async),
            self.auto_login_method(self.oroshiuri_instance.auto_login_oroshiuri_async),
            self.auto_login_method(self.petpochitto_instance.auto_login_petpochitto_async),
            self.auto_login_method(self.tajimaya_instance.auto_login_tajimaya_async)
        )

# if __name__ == "__main__":
#     pal = ParallelAutoLogin()
#     asyncio.run(pal.parallel_auto_login())