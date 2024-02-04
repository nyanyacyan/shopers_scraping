# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス 卸売ドットコムクラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper_ver2 import ScraperVer2

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperOroshiuri(ScraperVer2):
    def __init__(self, chrome, debug_mode=False):
        super().__init__(chrome, debug_mode=debug_mode)

        self.chrome = chrome

        self.oroshiuri_search_field_xpath = "//div[@class='__body']//input[@name='keyword']"  # search_field_xpath
        self.oroshiuri_search_button_xpath = "//div[@class='__body']//button[@class='__button c-button btn_header-search']"  # search_button_xpath
        self.oroshiuri_showcase_box_xpath = "//ul[@class='__product']//h2[@class='__title']"  # showcase_box_xpath
        self.oroshiuri_jump_link_xpath = "//ul[@class='__product']//h2[@class='__title']"  # jump_link_xpath
        self.oroshiuri_price_xpath = "//td[@class='__price']//span[@class='c-tax-price __tax-price __is-none']"  # price_xpath

    # search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, jump_link_xpath, price_xpath
    def scraper_oroshiuri(self, search_word):
        self.scraper_ver2(
            self.oroshiuri_search_field_xpath,
            search_word,
            self.oroshiuri_search_button_xpath,
            self.oroshiuri_showcase_box_xpath,
            self.oroshiuri_jump_link_xpath,
            self.oroshiuri_price_xpath,
        )