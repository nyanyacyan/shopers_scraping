# coding: utf-8
# ----------------------------------------------------------------------------------
# 非同期処理卸売ドットコム自動ログイン
# 2023/2/7制作


#---バージョン---
# Python==3.8.10

#---流れ--

# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from autologin.auto_login_async import AutoLogin
import asyncio

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginOroshiuri(AutoLogin):
    def __init__(self, chrome, debug_mode=False):
        super().__init__(chrome, debug_mode=debug_mode)

        self.chrome = chrome

        self.url_oroshiuri = os.getenv('URL_OROSHIURI')  # login_url
        self.id_oroshiuri = os.getenv('ID_OROSHIURI')  # userid
        self.password_oroshiuri = os.getenv('PASSWORD_OROSHIURI')  # password
        self.userid_xpath_oroshiuri = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_oroshiuri = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_oroshiuri = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_oroshiuri = "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # cart_element_xpath


    async def auto_login_oroshiuri_async(self):
        await self.auto_login_async(
            self.url_oroshiuri,
            self.id_oroshiuri,
            self.password_oroshiuri,
            self.userid_xpath_oroshiuri,
            self.password_xpath_oroshiuri,
            self.login_button_xpath_oroshiuri,
            self.cart_element_xpath_oroshiuri
        )
