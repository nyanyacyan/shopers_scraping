# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス Cookieログインクラス
# 2023/2/9制作

#---バージョン---
# Python==3.8.10

# １---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper_cookie_login import Scraper
from scraper.scraper_ver2_cookie import ScraperVer2
import os

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperNetsea(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.netsea_web_url = os.getenv("MAIN_URL_NETSEA")  # web_url
        self.netsea_cookies_file_name = "netsea_cookie_file.pkl"  # cookies_file_name
        self.netsea_cart_element_xpath = "//li[@class='header_cart_link']"  # cart_element_xpath
        self.netsea_search_field_xpath = "//input[@id='searchInput']"  # search_field_xpath
        self.netsea_showcase_box_xpath = "//div[@class='showcaseWrap gridView']"  # showcase_box_xpath
        self.netsea_price_xpath = "//div[@class='priceBox']//p[@class='afterPrice']"  # price_xpath
        self.netsea_url_xpath = "//section[@class='showcaseType01']//a[@class='flywheel_event']"  # url_xpath

    #  web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath
    async def scraper_netsea_async(self, search_word):
        result = await self.scraper_async(
            self.netsea_web_url,
            self.netsea_cookies_file_name,
            self.netsea_cart_element_xpath,
            self.netsea_search_field_xpath,
            search_word,
            self.netsea_showcase_box_xpath,
            self.netsea_price_xpath,
            self.netsea_url_xpath
        )
        return result
    
# ２---------------------------------------------------------------------------------------------------------

class ScraperOroshiuri(ScraperVer2):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.oroshiuri_web_url = os.getenv("MAIN_URL_OROSHIURI")  # web_url
        self.oroshiuri_cookies_file_name = "oroshiuri_cookie_file.pkl"  # cookies_file_name
        self.oroshiuri_cart_element_xpath = "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # cart_element_xpath
        self.oroshiuri_search_field_xpath = "//div[@class='__body']//input[@name='keyword']"  # search_field_xpath
        self.oroshiuri_showcase_box_xpath = "//ul[@class='__product']//h2[@class='__title']"  # showcase_box_xpath
        self.oroshiuri_jump_link_xpath = "//ul[@class='__product']//h2[@class='__title']"  # jump_link_xpath
        self.oroshiuri_price_xpath = "//td[@class='__price']//span[@class='c-tax-price __tax-price __is-none']"  # price_xpath


    #  web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath
    async def scraper_oroshiuri_async(self, search_word):
        result = await self.scraper_ver2_async(
            self.oroshiuri_web_url,
            self.oroshiuri_cookies_file_name,
            self.oroshiuri_cart_element_xpath,
            self.oroshiuri_search_field_xpath,
            search_word,
            self.oroshiuri_showcase_box_xpath,
            self.oroshiuri_jump_link_xpath,
            self.oroshiuri_price_xpath,
            # self.oroshiuri_url_xpath  # 商品ページに行く必要があるためなし
        )
        return result
    

    # 3---------------------------------------------------------------------------------------------------------


class ScraperPetpochitto(ScraperVer2):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.petpochitto_web_url = os.getenv("URL_PETPOCHITTO")  # web_url
        self.petpochitto_cookies_file_name = "petpochitto_cookie_file.pkl"  # cookies_file_name
        self.petpochitto_cart_element_xpath = "//a[contains(@href, 'cart')]//img[contains(@src, 'cart')]"  # cart_element_xpath
        self.petpochitto_search_field_xpath = "//input[@id='keyword' and @placeholder='商品名・キーワード・商品番号']"  # search_field_xpath
        self.petpochitto_showcase_box_xpath = "//div[@class='__item-count']"  # showcase_box_xpath
        self.oroshiuri_jump_link_xpath = "//h2[@class='__title']"  # jump_link_xpath
        self.petpochitto_price_xpath = "//div[@class='__total']//span[@class='c-tax-price __tax-price __is-none']"  # price_xpath


    async def scraper_petpochitto_async(self, search_word):
        result = await self.scraper_async(
            self.petpochitto_web_url,
            self.petpochitto_cookies_file_name,
            self.petpochitto_cart_element_xpath,
            self.petpochitto_search_field_xpath,
            search_word,
            self.petpochitto_showcase_box_xpath,
            self.oroshiuri_jump_link_xpath,
            self.petpochitto_price_xpath,
            # self.petpochitto_url_xpath  商品サイトまで行かないと見れないため
        )
        return result
    

# 4---------------------------------------------------------------------------------------------------------
    

class ScraperSuperDelivery(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.super_delivery_web_url = os.getenv("URL_SUPER_DELIVERY")  # web_url
        self.super_delivery_cookies_file_name = "super_delivery_cookie_file.pkl"  # cookies_file_name
        self.super_delivery_cart_element_xpath = "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"  # cart_element_xpath
        self.super_delivery_search_field_xpath = ""  # search_field_xpath
        self.super_delivery_showcase_box_xpath = ""  # showcase_box_xpath
        self.super_delivery_price_xpath = ""  # price_xpath


    async def scraper_super_delivery_async(self, search_word):
        result = await self.scraper_async(
            self.super_delivery_web_url,
            self.super_delivery_cookies_file_name,
            self.super_delivery_cart_element_xpath,
            self.super_delivery_search_field_xpath,
            search_word,
            self.super_delivery_showcase_box_xpath,
            self.super_delivery_price_xpath,
            self.super_delivery_url_xpath
        )
        return result
    

# 5---------------------------------------------------------------------------------------------------------
    

class ScraperTajimaya(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.tajimaya_web_url = os.getenv("URL_TAJIMAYA")  # web_url
        self.tajimaya_cookies_file_name = "tajimaya_cookie_file.pkl"  # cookies_file_name
        self.tajimaya_cart_element_xpath = "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"  # cart_element_xpath
        self.tajimaya_search_field_xpath = ""  # search_field_xpath
        self.tajimaya_showcase_box_xpath = ""  # showcase_box_xpath
        self.tajimaya_price_xpath = ""  # price_xpath


    async def scraper_tajimaya_async(self, search_word):
        result = await self.scraper_async(
            self.tajimaya_web_url,
            self.tajimaya_cookies_file_name,
            self.tajimaya_cart_element_xpath,
            self.tajimaya_search_field_xpath,
            search_word,
            self.tajimaya_showcase_box_xpath,
            self.tajimaya_price_xpath,
            self.tajimaya_url_xpath
        )
        return result
    

# ---------------------------------------------------------------------------------------------------------