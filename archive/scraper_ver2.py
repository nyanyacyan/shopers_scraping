from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os
import re

from logger.debug_logger import Logger

load_dotenv()

class ScraperVer2:
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



    def scraper_ver2(self, search_field_xpath, search_word, search_button_xpath, showcase_box_xpath, jump_link_xpath, price_xpath):
        '''
        autologinにてサイトが開かれてる状態
        => 検索バーへスプシからのデータを入力して検索
        => 開いたサイトから
        '''
        try:
            # 検索バーを探して入力
            self.logger.debug("検索バーを特定開始")
            search_field = self.chrome.find_element_by_xpath(search_field_xpath)
            search_field.send_keys(search_word)
            self.logger.debug("検索バーを発見")

            # 検索ボタンを探す
            self.logger.debug("buttanサーチ開始")
            login_button = self.chrome.find_element_by_xpath(search_button_xpath)
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
            # 商品ページ（showcasecasebox）があるかどうかを確認
            self.logger.debug("商品が存在するか確認。")
            self.chrome.find_element_by_xpath(showcase_box_xpath)
            self.logger.debug("商品が存在してるのを確認できました。")


            # リンクへジャンプできる箇所を捜索
            try:
                self.logger.debug("リンク貼り付け箇所を捜索開始")
                jump_link = self.chrome.find_element_by_xpath(jump_link_xpath)
                jump_link.click()
                self.logger.debug("リンク貼り付け箇所を捜索完了")

            except NoSuchElementException as e:
                self.logger.error("リンクが貼り付けてる箇所が見つけられませんでした。")
                raise ("ジャンプリンクが見つかりませんでした。")


            # ページが完全に読み込まれるまで待機
            self.logger.debug("ページが読み込み完了してるかを確認中")
            WebDriverWait(self.chrome, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.logger.debug("ページは完全に表示されてる")


            # 価格要素抽出
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

            # 現在のURLを取得
            self.url = self.chrome.current_url

        # showcaseがなかった場合は商品がない
        except:
            self.logger.error("商品の該当なし")
            return "該当なし"

    # オーバーライド
    # 各種の変数を召喚用に作成したメソッド
    def get_price(self):
        return self.price
    
    def get_url(self):
        return self.url