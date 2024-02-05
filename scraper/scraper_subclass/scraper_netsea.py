# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス Netseaクラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper import Scraper

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperNetsea(Scraper):
    def __init__(self, chrome, debug_mode=False):
        super().__init__(chrome, debug_mode=debug_mode)

        self.chrome = chrome

        self.netsea_search_field_xpath = "//input[@id='searchInput']"  # search_field_xpath
        self.netsea_search_button_xpath = "//div[@class='searchSubmit']/button[@id='searchBtn' and @class='searchBtn']"  # search_button_xpath
        self.netsea_showcase_box_xpath = "//section[@class='showcaseWrap gridView']"  # showcase_box_xpath
        self.netsea_price_xpath = "//section[@class='showcaseType01']//p[@class='price']"  # price_xpath
        self.netsea_url_xpath = "//section[@class='showcaseType01']//a[@class='flywheel_event']"  # url_xpath

    #  search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath
    def scraper_netsea(self, search_word):
        self.scraper(
            self.netsea_search_field_xpath,
            search_word,
            self.netsea_search_button_xpath,
            self.netsea_showcase_box_xpath,
            self.netsea_price_xpath,
            self.netsea_url_xpath
        )