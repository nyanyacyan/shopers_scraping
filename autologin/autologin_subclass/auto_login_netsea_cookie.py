# coding: utf-8
# ----------------------------------------------------------------------------------
# 非同期処理 netsea自動ログイン
# 2023/2/9制作


#---バージョン---
# Python==3.8.10

#---流れ--
# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os


from autologin.auto_login_cookie import AutoLogin

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
        self.cart_element_xpath_netsea = "//li[@class='header_cart_link']"  # cart_element_xpath
        self.remember_box_xpath_netsea = "//label[contains(text(), 'ブラウザを閉じてもログインしたままにする')]"  # remember_box_xpath
        self.cookies_file_name_netsea = "netsea_cookie_file.pkl"  # cookies_file_name


    async def auto_login_netsea_async(self):
        await self.auto_login_async(
            self.url_netsea,
            self.id_netsea,
            self.password_netsea,
            self.userid_xpath_netsea,
            self.password_xpath_netsea,
            self.login_button_xpath_netsea,
            self.cart_element_xpath_netsea,
            self.remember_box_xpath_netsea,
            self.cookies_file_name_netsea
        )
