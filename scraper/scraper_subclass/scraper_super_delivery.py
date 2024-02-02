# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング 子クラス SuperDeliveryクラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

# ---------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
from scraper.scraper import Scraper

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperSuperDelivery(Scraper):
    def __init__(self, debug_mode=False):
        super().__init__(debug_mode=debug_mode)

        self.super_delivery_sarch_field_xpath = ""  # sarch_field_xpath
        self.super_delivery_login_button_xpath = ""  # login_button_xpath
        self.super_delivery_show_box_xpath = ""  # show_box_xpath
        self.super_delivery_price_xpath = ""  # price_xpath
        self.super_delivery_image_xpath = ""  # image_xpath

    #  sarch_field_xpath, sarch_word, login_button_xpath, show_box_xpath, price_xpath, image_xpath
    def scraper_super_delivery(self, sarch_word):
        self.scraper(
            self.super_delivery_sarch_field_xpath,
            sarch_word,
            self.super_delivery_login_button_xpath,
            self.super_delivery_show_box_xpath,
            self.super_delivery_price_xpath,
            self.super_delivery_image_xpath
        )