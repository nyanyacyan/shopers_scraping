# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング Cookieが使えないクラス
# 2023/2/12制作

#---バージョン---
# Python==3.8.10

# webdriverはオートログインとスクレイピングを同時に行うクラスにて管理
# 今後オートログインクラスを別で作成→Cookie取得部分をなくす

# ---------------------------------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from scraper.scraper_ver2_async import ScraperVer2

load_dotenv()  # .env ファイルから環境変数を読み込む

class ScraperNocookieSuperDelivery(ScraperVer2):
    def __init__(self, chrome, debug_mode=False):
        super().__init__(chrome, debug_mode=debug_mode)

        self.chrome = chrome

        self.super_delivery_search_field_xpath = "//input[@id='header_word']"  # search_field_xpath
        self.super_delivery_showcase_box_xpath = "//div[@class='co-clf item-box-area']//div[@class='itembox-parts']"  # showcase_box_xpath
        self.super_delivery_search_buttan_xpath = "//div[@id='rwd-searchbox-button']/input[@type='submit']"  # search_buttan_xpath
        self.super_delivery_jump_link_xpath = "//div[@class='item-img-box wish-dvs-jdg item-wish']/a"  # 
        self.super_delivery_price_xpath = "//tr[@class='co-pc-only']//td[@class='maker-wholesale-set-price co-align-right']"  # price_xpath

    #  search_field_xpath, search_word, search_buttan_xpath, showcase_box_xpath, jump_link_xpath, price_xpath
    async def scraper_super_delivery_async(self, search_word):
        result = await self.scraper_ver2_async(
            self.super_delivery_search_field_xpath,
            search_word,
            self.super_delivery_search_buttan_xpath,
            self.super_delivery_showcase_box_xpath,
            self.super_delivery_jump_link_xpath,
            self.super_delivery_price_xpath
        )
        return result