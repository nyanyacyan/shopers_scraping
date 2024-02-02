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

class AutoLoginTajimaya(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)
        
        self.url_tajimaya = os.getenv('URL_TAJIMAYA')  # login_url
        self.id_tajimaya = os.getenv('ID_TAJIMAYA')  # userid
        self.password_tajimaya = os.getenv('PASSWORD_TAJIMAYA')  # password
        self.userid_xpath_tajimaya = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_tajimaya = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_tajimaya = "//input[@type='submit']"  # login_button_xpath
        self.cart_element_xpath_tajimaya = "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"  # cart_element_xpath

    # login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath
    def auto_login_Tajimaya(self):
        self.auto_login(
            self.url_tajimaya,
            self.id_tajimaya,
            self.password_tajimaya,
            self.userid_xpath_tajimaya,
            self.password_xpath_tajimaya,
            self.login_button_xpath_tajimaya,
            self.cart_element_xpath_tajimaya
        )
