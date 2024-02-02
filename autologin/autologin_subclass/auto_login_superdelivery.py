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

        self.url_super_delivery = os.getenv('URL_SUPER_DELIVERY')  # login_url
        self.id_super_delivery = os.getenv('ID_SUPER_DELIVERY')  # userid
        self.password_super_delivery = os.getenv('PASSWORD_SUPER_DELIVERY')  # password
        self.userid_xpath_super_delivery = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_super_delivery = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_super_delivery = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_super_delivery = "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"  # cart_element_xpath


    def auto_login_super_delivery(self):
        self.auto_login(
            self.url_super_delivery,
            self.id_super_delivery,
            self.password_super_delivery,
            self.userid_xpath_super_delivery,
            self.password_xpath_super_delivery,
            self.login_button_xpath_super_delivery,
            self.cart_element_xpath_super_delivery
        )
