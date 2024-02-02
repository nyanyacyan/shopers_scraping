# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス 卸売ドットコムクラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper import Scraper

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperOroshiuri(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.oroshiuri_search_field_xpath = ""  # search_field_xpath
        self.oroshiuri_search_button_xpath = ""  # search_button_xpath
        self.oroshiuri_showcase_box_xpath = ""  # showcase_box_xpath
        self.oroshiuri_price_xpath = ""  # price_xpath
        self.oroshiuri_image_xpath = ""  # image_xpath

    #  search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, image_xpath
    def scraper_oroshiuri(self, search_word):
        self.scraper(
            self.oroshiuri_search_field_xpath,
            search_word,
            self.oroshiuri_search_button_xpath,
            self.oroshiuri_showcase_box_xpath,
            self.oroshiuri_price_xpath,
            self.oroshiuri_image_xpath
        )