# ----------------------------------------------------------------------------------
# SUPER DELIVERY　自動ログイン
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

class AutoLoginSuperDelivery(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)


    def auto_login_super_delivery(self):
        url_super_delivery = os.getenv('URL_SUPER_DELIVERY')
        id_super_delivery = os.getenv('ID_SUPER_DELIVERY')
        password_super_delivery = os.getenv('PASSWORD_SUPER_DELIVERY')

        self.auto_login(
            url_super_delivery,
            id_super_delivery,
            password_super_delivery,
            "//input[@name='loginEmail']",
            "//input[@name='loginPassword']",
            "//input[@name='login']",
            "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"
        )
