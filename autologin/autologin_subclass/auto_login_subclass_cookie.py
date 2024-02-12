# coding: utf-8
# ----------------------------------------------------------------------------------
# 非同期処理 Cookie保存クラス
# 自動ログインするためのCookieを取得
# 今後、サイトを追加する場合にはクラスを追加していく=> 増え過ぎた場合は別ファイルへ

# 2023/2/9制作

# １----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os

# 自作モジュール
from autologin.auto_login_cookie import AutoLogin

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginNetsea(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.site_name = "NETSEA"
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
            self.site_name,
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


# ２----------------------------------------------------------------------------------


from dotenv import load_dotenv
import os

# 自作モジュール
from autologin.auto_login_cookie import AutoLogin

load_dotenv()  # .env ファイルから環境変数を読み込む

class AutoLoginOroshiuri(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.site_name = "卸売ドットコム"
        self.url_oroshiuri = os.getenv('URL_OROSHIURI')  # login_url
        self.id_oroshiuri = os.getenv('ID_OROSHIURI')  # userid
        self.password_oroshiuri = os.getenv('PASSWORD_OROSHIURI')  # password
        self.userid_xpath_oroshiuri = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_oroshiuri = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_oroshiuri = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_oroshiuri = "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # cart_element_xpath
        self.remember_box_xpath_oroshiuri = "//label[contains(text(), ' ログイン状態を保存する')]"  # remember_box_xpath
        self.cookies_file_name_oroshiuri = "oroshiuri_cookie_file.pkl"  # cookies_file_name


    async def auto_login_oroshiuri_async(self):
        await self.auto_login_async(
            self.site_name,
            self.url_oroshiuri,
            self.id_oroshiuri,
            self.password_oroshiuri,
            self.userid_xpath_oroshiuri,
            self.password_xpath_oroshiuri,
            self.login_button_xpath_oroshiuri,
            self.cart_element_xpath_oroshiuri,
            self.remember_box_xpath_oroshiuri,
            self.cookies_file_name_oroshiuri
        )


# ３----------------------------------------------------------------------------------


class AutoLoginPetpochitto(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.site_name = "ペットポチッと"
        self.url_petpochitto = os.getenv('URL_PETPOCHITTO')  # login_url
        self.id_petpochitto = os.getenv('ID_PETPOCHITTO')  # userid
        self.password_petpochitto = os.getenv('PASSWORD_PETPOCHITTO')  # password
        self.userid_xpath_petpochitto = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_petpochitto = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_petpochitto = "//input[@name='login']"  # login_button_xpath
        self.cart_element_xpath_petpochitto = "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"  # cart_element_xpath
        self.remember_box_xpath_petpochitto = "//label[contains(text(), ' ログイン状態を保存する')]"  # remember_box_xpath
        self.cookies_file_name_petpochitto = "petpochitto_cookie_file.pkl"  # cookies_file_name


    async def auto_login_petpochitto_async(self):
        await self.auto_login_async(
            self.site_name,
            self.url_petpochitto,
            self.id_petpochitto,
            self.password_petpochitto,
            self.userid_xpath_petpochitto,
            self.password_xpath_petpochitto,
            self.login_button_xpath_petpochitto,
            self.cart_element_xpath_petpochitto,
            self.remember_box_xpath_petpochitto,
            self.cookies_file_name_petpochitto
        )


# ４----------------------------------------------------------------------------------


class AutoLoginSuperDelivery(AutoLogin):
    def __init__(self, chrome, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.chrome = chrome

        self.site_name = "SuperDelivery"
        self.url_super_delivery = os.getenv('URL_SUPER_DELIVERY')  # login_url
        self.id_super_delivery = os.getenv('ID_SUPER_DELIVERY')  # userid
        self.password_super_delivery = os.getenv('PASSWORD_SUPER_DELIVERY')  # password
        self.userid_xpath_super_delivery = "//input[@name='identification']"  # userid_xpath
        self.password_xpath_super_delivery = "//input[@name='password']"  # password_xpath
        self.login_button_xpath_super_delivery = "//div[@class='co-btn co-btn-red co-btn-m co-btn-page']//input[@type='submit'][@value='ログイン']"  # login_button_xpath
        self.cart_element_xpath_super_delivery = "//td[@id='price-btn-area']"  # cart_element_xpath
        self.remember_box_xpath_super_delivery = ""  # remember_box_xpath　なし
        self.cookies_file_name_super_delivery = "super_delivery_cookie_file.pkl"  # cookies_file_name


    async def auto_login_super_delivery_async(self):
        await self.auto_login_async(
            self.site_name,
            self.url_super_delivery,
            self.id_super_delivery,
            self.password_super_delivery,
            self.userid_xpath_super_delivery,
            self.password_xpath_super_delivery,
            self.login_button_xpath_super_delivery,
            self.cart_element_xpath_super_delivery,
            self.remember_box_xpath_super_delivery,
            self.cookies_file_name_super_delivery
        )


# 4----------------------------------------------------------------------------------


class AutoLoginTajimaya(AutoLogin):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.site_name = "Tajimaya"
        self.url_tajimaya = os.getenv('URL_TAJIMAYA')  # login_url
        self.id_tajimaya = os.getenv('ID_TAJIMAYA')  # userid
        self.password_tajimaya = os.getenv('PASSWORD_TAJIMAYA')  # password
        self.userid_xpath_tajimaya = "//input[@name='loginEmail']"  # userid_xpath
        self.password_xpath_tajimaya = "//input[@name='loginPassword']"  # password_xpath
        self.login_button_xpath_tajimaya = "//input[@type='submit']"  # login_button_xpath
        self.cart_element_xpath_tajimaya = "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"  # cart_element_xpath
        self.remember_box_xpath_tajimaya = "//div[@class='__remember']//input[@name='remember']"  # remember_box_xpath
        self.cookies_file_name_tajimaya = "tajimaya_cookie_file.pkl"  # cookies_file_name


    async def auto_login_tajimaya_async(self):
        await self.auto_login_async(
            self.site_name,
            self.url_tajimaya,
            self.id_tajimaya,
            self.password_tajimaya,
            self.userid_xpath_tajimaya,
            self.password_xpath_tajimaya,
            self.login_button_xpath_tajimaya,
            self.cart_element_xpath_tajimaya,
            self.remember_box_xpath_tajimaya,
            self.cookies_file_name_tajimaya
        )


# ----------------------------------------------------------------------------------
