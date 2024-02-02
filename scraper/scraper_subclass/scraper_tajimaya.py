# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス Tajimayaクラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper import Scraper

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperTajimaya(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.tajimaya_search_field_xpath = ""  # search_field_xpath
        self.tajimaya_search_button_xpath = ""  # search_button_xpath
        self.tajimaya_showcase_box_xpath = ""  # showcase_box_xpath
        self.tajimaya_price_xpath = ""  # price_xpath
        self.tajimaya_image_xpath = ""  # image_xpath

    #  search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, image_xpath
    def scraper_tajimaya(self, search_word):
        self.scraper(
            self.tajimaya_search_field_xpath,
            search_word,
            self.tajimaya_search_button_xpath,
            self.tajimaya_showcase_box_xpath,
            self.tajimaya_price_xpath,
            self.tajimaya_image_xpath
        )