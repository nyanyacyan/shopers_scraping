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

        self.url_oroshiuri = os.getenv('URL_OROSHIURI')  # login_url
        self.id_oroshiuri = os.getenv('ID_OROSHIURI')  # userid
        self.password_oroshiuri = os.getenv('PASSWORD_OROSHIURI')  # password
        self.userid_xpath_oroshiuri = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_oroshiuri = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_oroshiuri = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_oroshiuri = "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # cart_element_xpath


    def auto_login_oroshiuri(self):
        self.auto_login(
            self.url_oroshiuri,
            self.id_oroshiuri,
            self.password_oroshiuri,
            self.userid_xpath_oroshiuri,
            self.password_xpath_oroshiuri,
            self.login_button_xpath_oroshiuri,
            self.cart_element_xpath_oroshiuri
        )
