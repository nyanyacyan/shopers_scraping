from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import pickle
import os
import re
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
import functools
import time

from logger.debug_logger import Logger

load_dotenv()

executor = ThreadPoolExecutor(max_workers=5)

class SingleItemScraper:
    def __init__(self, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
        chrome_options.add_argument("--window-size=1680,1200")  # ウィンドウサイズの指定

        # ChromeDriverManagerを使用して自動的に適切なChromeDriverをダウンロードし、サービスを設定
        service = Service(ChromeDriverManager().install())

        # WebDriverインスタンスを生成
        self.chrome = webdriver.Chrome(service=service, options=chrome_options)

        # データ格納するための箱
        self.price = None
        self.url = None



    def single_item_scraper(self, web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, showcase_box_xpath, jump_link_xpath, price_xpath):
        '''
        Cookieを使ってログインしてログイン状態をキープして繰り返しスクレイピング。
        '''
        # ログインされた後のメインURLを設定
        web_url = web_url

        # 保存してあるCookieファイルを選定
        cookies_file_name = cookies_file_name

        # Cookieファイルを展開
        try:
            cookies = pickle.load(open('/Users/nyanyacyan/Desktop/ProgramFile/project_file/shopers_scraping/scraper/scraper_subclass/cookies/' + cookies_file_name, 'rb'))

        except FileNotFoundError as e:
            self.logger.error(f"ファイルが見つかりません:{e}")

        except Exception as e:
            self.logger.error(f"処理中にエラーが起きました:{e}")

        self.chrome.get(web_url)
        self.logger.info("メイン画面にアクセス")

        # Cookieを設定
        for c in cookies:
            self.chrome.add_cookie(c)

        self.chrome.get(web_url)
        self.logger.info("Cookieを使ってメイン画面にアクセス")


        if web_url != self.chrome.current_url:
            self.logger.info("Cookieでのログイン成功")

        else:
            self.logger.info("Cookieでのログイン失敗")
            session = requests.Session()

            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

            response = session.get(web_url)
            if "ログイン成功の条件" in response.text:
                self.logger.info("requestsによるCookieでのログイン成功")
            else:
                self.logger.info("requestsによるCookieでのログイン失敗")



        try:
            self.chrome.find_element_by_xpath(cart_element_xpath)
            self.logger.info("ログイン完了")

        except NoSuchElementException as e:
            self.logger.error(f"ログインができてない。{e}")

        
        try:
            # 検索バーを探して入力
            self.logger.debug("検索バーを特定開始")
            search_field = self.chrome.find_element_by_xpath(search_field_xpath)
            self.logger.debug("検索バーを発見")

            time.sleep(3)
            
            self.logger.debug("検索ワード入力開始")
            search_field.send_keys(search_word)
            self.logger.debug("検索ワード入力完了")

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
            self.logger.debug("商品が存在するか確認。")
            self.chrome.find_element_by_xpath(showcase_box_xpath)
            self.logger.debug("商品が存在してるのを確認できました。")


            # リンクへジャンプできる箇所を捜索
            try:
                self.logger.debug("リンク貼り付け箇所を捜索開始")
                jump_link = self.chrome.find_element_by_xpath(jump_link_xpath)
                self.logger.debug("リンク貼り付け箇所を捜索完了")

                old_url = self.chrome.current_url

                # jump_link.click()
                self.chrome.execute_script("arguments[0].click();", jump_link)

                time.sleep(3)

                new_url = self.chrome.current_url

                if new_url != old_url:
                    self.logger.debug("ページ遷移成功")
                else:
                    self.logger.error("ページ遷移失敗")


            except NoSuchElementException as e:
                self.logger.error("リンクが貼り付けてる箇所が見つけられませんでした。")
                raise ("ジャンプリンクが見つかりませんでした。")


            # ページが完全に読み込まれるまで待機
            self.logger.debug("ページが読み込み完了してるかを確認中")
            WebDriverWait(self.chrome, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.logger.debug("ページは完全に表示されてる")


            self.chrome.save_screenshot('price_before.png')



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
                    price_without_comma = re.sub("[^\d.]", "", price_text)
                    clean_price = float(price_without_comma)
                    self.logger.debug(f"価格の抽出完了:{clean_price}")
                    self.price = clean_price

                except ValueError:
                    self.logger.error(f"価格のクリーニングに失敗: {price_without_comma}")
                    self.price = None

            except Exception as e:
                self.logger.error(f"pricesの処理中にエラー:{e}")

            # 現在のURLを取得
            self.url = self.chrome.current_url
            self.logger.debug(self.url)

        # showcaseがなかった場合は商品がない
        except NoSuchElementException:
            self.logger.error("商品の該当なし")
            self.price = "該当なし"
            self.url = None


        # 同期メソッドを非同期処理に変換
    async def single_item_scraper_async(self, web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, showcase_box_xpath, jump_link_xpath, price_xpath):
        loop = asyncio.get_running_loop()

        # ブロッキング、実行タイミング、並列処理などを適切に行えるように「functools」にてワンクッション置いて実行
        await loop.run_in_executor(executor, functools.partial(self.single_item_scraper, web_url, cookies_file_name, cart_element_xpath, search_field_xpath, search_word, showcase_box_xpath, jump_link_xpath, price_xpath))
        self.logger.debug(f"scraper execution finished: price={self.price}, url={self.url}")
        result = {
            "price": self.price,
            "url": self.url
        }
        self.logger.debug(f"search_word: {search_word}")

        self.logger.debug(f"result: {result}")

        return result