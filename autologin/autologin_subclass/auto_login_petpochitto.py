# coding: utf-8
# ----------------------------------------------------------------------------------
# PETポチッと　自動ログイン
# 2023/1/20制作

#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from auto_login_headless import AutoLogin

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginPetpochitto(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)


    def auto_login_petpochitto(self):
        url_petpochitto = os.getenv('URL_PETPOCHITTO')
        id_petpochitto = os.getenv('ID_PETPOCHITTO')
        password_petpochitto = os.getenv('PASSWORD_PETPOCHITTO')

        self.auto_login(
            url_petpochitto,
            id_petpochitto,
            password_petpochitto,
            "//input[@name='loginEmail']",
            "//input[@name='loginPassword']",
            "//input[@name='login']",
            "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"
        )
