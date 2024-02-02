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

        self.url_netsea = os.getenv('URL_NETSEA')  # login_url
        self.id_netsea = os.getenv('ID_NETSEA')  # userid
        self.password_netsea = os.getenv('PASSWORD_NETSEA')  # password
        self.userid_xpath_netsea = "//input[@name='login_id']"  # userid_xpath
        self.password_xpath_netsea = "//input[@name='password']"  # password_xpath
        self.login_button_xpath_netsea = "//button[@name='submit']"  # login_button_xpath
        self.cart_element_xpath_netsea = "/a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # cart_element_xpath


    def auto_login_netsea(self):
        self.auto_login(
            self.url_netsea,
            self.id_netsea,
            self.password_netsea,
            self.userid_xpath_netsea,
            self.password_xpath_netsea,
            self.login_button_xpath_netsea,
            self.cart_element_xpath_netsea
        )
