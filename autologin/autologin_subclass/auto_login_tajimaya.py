# coding: utf-8
# ----------------------------------------------------------------------------------
# Tajimaya　自動ログイン
# 2023/2/2制作
# reCAPTCHA有り

#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from auto_login_headless import AutoLogin

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginSuperDelivery(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)


    def auto_login_Tajimaya(self):
        url_tajimaya = os.getenv('URL_TAJIMAYA')
        id_tajimaya = os.getenv('ID_TAJIMAYA')
        password_tajimaya = os.getenv('PASSWORD_TAJIMAYA')

        self.auto_login(
            url_tajimaya,
            id_tajimaya,
            password_tajimaya,
            "//input[@name='loginEmail']",
            "//input[@name='loginPassword']",
            "//input[@type='submit']",
            "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"
        )
