# coding: utf-8
# ---------------------------------------------------------------------------------------------------------
# スクレイピング クラス
# 2023/2/1制作

#---バージョン---
# Python==3.8.10

#---流れ--
# それぞれの子クラスにて抽出先を決定して実行できるようにする=> 新しいスクレイピング先には子クラスの作成が必要
# 入力項目=> 日付=> 画像=> JAN=> 商品名=> 価格=> URL
# ---------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os

# 自作モジュール
from logger.debug_logger import Logger
from spreadsheet.read import Spreadsheet_read

load_dotenv()

class Scraper:
    def __init__(self, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        self.mix_data = Spreadsheet_read(debug_mode=debug_mode)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1680,780")

        service = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=service, options=chrome_options)


    def scraper(self, sarch_field_xpath, sarch_word, login_button_xpath, show_box_xpath, price_xpath, image_xpath):
        '''
        autologinにてサイトが開かれてる状態
        => 検索バーへスプシからのデータを入力して検索
        => 開いたサイトから
        '''
        try:
            # 検索バーを探して入力
            self.logger.debug("検索バーを特定開始")
            sarch_field = self.chrome.find_element_by_xpath(sarch_field_xpath)
            sarch_field.send_keys(sarch_word)
            self.logger.debug("検索バーを発見")

            # 検索ボタンを探す
            self.logger.debug("buttanサーチ開始")
            login_button = self.chrome.find_element_by_xpath(login_button_xpath)
            self.logger.debug("buttanサーチ、OK")


            # 検索ボタンを押す
            self.logger.debug("クリック開始")
            self.chrome.execute_script("arguments[0].click();", login_button)
            self.logger.debug("クリック完了")

        except NoSuchElementException as e:
            self.logger.error(f"検索バーが見つかりません:{e}")


        # ページが完全に読み込まれるまで待機
        self.logger.debug("ページが読み込み完了してるかを確認中")
        WebDriverWait(self.chrome, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("ページは完全に表示されてる")


        try:
            # 商品ページ（showbox）があるかどうかを確認
            self.chrome.find_elements_by_xpath(show_box_xpath)

            try:
                # 商品をなるべく厳選できるpathを用意する
                self.logger.debug('priceの捜索開始')
                price_elements = self.chrome.find_elements_by_xpath(price_xpath)
                prices = []

                self.logger.debug("pricesの解析とクリーニング開始")
                for element in price_elements:
                    price_text = element.text
                    price_without_comma = price_text.replace(",", "")
                    price_int_change = int(price_without_comma)

                    prices.append(price_int_change)
                
                self.logger.debug(prices)

                if len(prices) > 2:
                    raise ValueError("価格データが複数あり、特定できてません。")
                
                if not prices:
                    raise ValueError("価格データが見つかりませんでした。")

                self.logger.debug("価格の抽出完了")

            except NoSuchElementException as e:
                self.logger.debug(f"価格が見つかりません:{e}")

            except Exception as e:
                self.logger.error(f"pricesの処理中にエラー:{e}")


            try:
                # 画像の場所を特定して変数化
                # 画像のURLを特定する
                # １枚目のみ表示
                self.logger.debug("画像の捜索開始")
                image_elements = self.chrome.find_elements_by_xpath(image_xpath)
                image_urls = []

                # 画像の解析開始
                for image_element in image_elements:
                    image_url = image_element.get_attribute("src")

                    image_urls.append(image_url)

                self.logger.debug(f"'image_url:'{image_urls}")

                if len(image_urls) > 2:
                    self.logger.error('画像URLが複数あり、特定できてません')
                
                if not image_urls:
                    self.logger.error("画像データが見つからなかった")
                
                self.logger.debug("画像URLの抽出完了")

                # URLを入手
                current_url = self.chrome.current_url
                self.logger.debug(current_url)
                self.logger.debug("URLの抽出完了")

            except Exception as e:
                self.logger.error("処理中にエラーが発生:{e}")

        except:
            self.logger.debug("商品の該当なし")
            return "該当なし"
