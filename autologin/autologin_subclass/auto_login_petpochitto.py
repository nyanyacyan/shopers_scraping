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

        self.url_petpochitto = os.getenv('URL_PETPOCHITTO')  # login_url
        self.id_petpochitto = os.getenv('ID_PETPOCHITTO')  # userid
        self.password_petpochitto = os.getenv('PASSWORD_PETPOCHITTO')  # password
        self.userid_xpath_petpochitto = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_petpochitto = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_petpochitto = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_petpochitto = "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"  # cart_element_xpath


    def auto_login_petpochitto(self):
        self.auto_login(
            self.url_petpochitto,
            self.id_petpochitto,
            self.password_petpochitto,
            self.userid_xpath_petpochitto,
            self.password_xpath_petpochitto,
            self.login_button_xpath_petpochitto,
            self.cart_element_xpath_petpochitto
        )
