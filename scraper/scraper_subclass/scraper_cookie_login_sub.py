# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス Cookieログインクラス
# 2023/2/9制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper_cookie_login import Scraper

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperNetsea(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.web_url = "https://www.netsea.jp/"# web_url
        self.cookies_file_name_netsea = "netsea_cookie_file.pkl"  # cookies_file_name
        self.cart_element_xpath_netsea = "//li[@class='header_cart_link']"  # cart_element_xpath
        self.netsea_search_field_xpath = "//input[@id='searchInput']"  # search_field_xpath
        self.netsea_showcase_box_xpath = "//div[@class='showcaseWrap gridView']"  # showcase_box_xpath
        self.netsea_price_xpath = "//div[@class='priceBox']//p[@class='afterPrice']"  # price_xpath
        self.netsea_url_xpath = "//section[@class='showcaseType01']//a[@class='flywheel_event']"  # url_xpath

    #  web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath
    async def scraper_netsea_async(self, search_word):
        result = await self.scraper_async(
            self.web_url,
            self.cookies_file_name_netsea,
            self.cart_element_xpath_netsea,
            self.netsea_search_field_xpath,
            search_word,
            self.netsea_showcase_box_xpath,
            self.netsea_price_xpath,
            self.netsea_url_xpath
        )
        return result