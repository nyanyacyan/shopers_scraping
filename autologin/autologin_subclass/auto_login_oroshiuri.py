# ----------------------------------------------------------------------------------
# 卸売ドットコム自動ログイン
# 2023/2/2制作


#---バージョン---
# Python==3.8.10

#---流れ--
# ID入力=> パス入力=> クリック
# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from auto_login_headless import AutoLogin

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginOroshiuri(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)


    def auto_login_oroshiuri(self):
        url_oroshiuri = os.getenv('URL_OROSHIURI')
        id_oroshiuri = os.getenv('ID_OROSHIURI')
        password_oroshiuri = os.getenv('PASSWORD_OROSHIURI')

        self.auto_login(
            url_oroshiuri,
            id_oroshiuri,
            password_oroshiuri,
            "//input[@name='loginEmail']",
            "//input[@name='loginPassword']",
            "//input[@name='login']",
            "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"
        )
