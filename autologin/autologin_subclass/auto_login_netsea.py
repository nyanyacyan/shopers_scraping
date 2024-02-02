# coding: utf-8
# ----------------------------------------------------------------------------------
# netsea自動ログイン
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

class AutoLoginNetsea(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)


    def auto_login_netsea(self):
        url_netsea = os.getenv('URL_NETSEA')
        id_netsea = os.getenv('ID_NETSEA')
        password_netsea = os.getenv('PASSWORD_NETSEA')

        self.auto_login(
            url_netsea,
            id_netsea,
            password_netsea,
            "//input[@name='login_id']",
            "//input[@name='password']",
            "//button[@name='submit']",
            "/a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"
        )