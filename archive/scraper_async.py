# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# 非同期スクレイピング クラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

#---流れ--
# それぞれの子クラスにて抽出先を決定して実行できるようにする=> 新しいスクレイピング先には子クラスの作成が必要
# 入力項目=> 日付=> 画像=> JAN=> 商品名=> 価格=> URL
# ---------------------------------------------------------------------------------------------------------
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import re
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
import time

# 自作モジュール
from logger.debug_logger import Logger

load_dotenv()

executor = ThreadPoolExecutor(max_workers=5)

class Scraper:
    def __init__(self, chrome, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        self.chrome = chrome

        # データ格納するための箱
        self.price = None
        self.url = None


    def scraper(self, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath):
        '''
        autologinにてサイトが開かれてる状態
        => 検索バーへスプシからのデータを入力して検索
        => 開いたサイトから
        '''
        try:
            # 検索バーを探して入力
            self.logger.debug("検索バーを特定開始")
            search_field = self.chrome.find_element_by_xpath(search_field_xpath)
            self.logger.debug("検索バーを発見")

            self.logger.debug("検索バーに入力開始")
            search_field.send_keys(search_word)
            
            self.logger.debug("検索バーに入力完了")

            time.sleep(1)
            
            # エンターキーを入力
            search_field.send_keys(Keys.ENTER)

            # # 検索ボタンを探す
            # self.logger.debug("buttanサーチ開始")
            # login_button = self.chrome.find_element_by_xpath(search_button_xpath)
            # self.logger.debug("buttanサーチ、OK")

            # # 検索ボタンを押す
            # self.logger.debug("クリック開始")
            # self.chrome.execute_script("arguments[0].click();", login_button)
            # self.logger.debug("クリック完了")

        except NoSuchElementException as e:
            self.logger.error(f"検索バーが見つかりません:{e}")


        # ページが完全に読み込まれるまで待機
        self.logger.debug("ページが読み込み完了してるかを確認中")
        WebDriverWait(self.chrome, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("ページは完全に表示されてる")


        try:
            # 商品ページ（showcasecasebox）があるかどうかを確認
            self.logger.debug(f"使用されるshowcase_box_xpath: {showcase_box_xpath}")
            self.logger.debug("商品あるか確認")
            self.chrome.find_element_by_xpath(showcase_box_xpath)
            self.logger.debug("商品がありました。")

            try:
                # 商品をなるべく厳選できるpathを用意する
                self.logger.debug('priceの捜索開始')
                price_elements = self.chrome.find_elements_by_xpath(price_xpath)
                if price_elements:
                    price_text = price_elements[0].text  # 最初の要素のテキストを取得
                    self.logger.debug(f"price捜索完了:{price_text}")
                else:
                    raise ValueError("価格要素が存在しません。")

                try:
                    self.logger.debug("pricesの解析とクリーニング開始")
                    price_without_comma = re.sub("[^\d]", "", price_text)
                    clean_price = int(price_without_comma)
                    self.logger.debug(f"価格の抽出完了:{clean_price}")
                    self.price = clean_price

                except ValueError:
                    self.logger.error(f"価格のクリーニングに失敗: {price_without_comma}")
                    self.price = None

            except Exception as e:
                self.logger.error(f"pricesの処理中にエラー:{e}")


            try:
                # URLを入手
                self.logger.debug("商品URLの捜索開始")
                url_elements = self.chrome.find_elements_by_xpath(url_xpath)

                if url_elements:
                    url = url_elements[0].get_attribute('href')
                else:
                    url = None

                self.url = url
                self.logger.debug(f"商品URLの抽出完了: {self.url}")
                self.logger.debug("商品URLの抽出完了")

            except Exception as e:
                self.logger.error(f"処理中にエラーが発生: {e}")
                
            # ここで各変数の値をログに出力
            self.logger.debug(f"最終的な価格: {self.price}")
            self.logger.debug(f"最終的な商品URL: {self.url}")

        
        except:
            self.logger.error("商品の該当なし")
            self.price = "該当なし"
            self.url = None

    # 同期メソッドを非同期処理に変換
    async def scraper_async(self, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath):
        loop = asyncio.get_running_loop()

        # ブロッキング、実行タイミング、並列処理などを適切に行えるように「functools」にてワンクッション置いて実行
        await loop.run_in_executor(executor, functools.partial(self.scraper, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, price_xpath, url_xpath))
        self.logger.debug(f"scraper execution finished: price={self.price}, url={self.url}")
        result = {
            "price": self.price,
            "url": self.url
        }
        self.logger.debug(f"search_word: {search_word}")

        self.logger.debug(f"result: {result}")


        return result