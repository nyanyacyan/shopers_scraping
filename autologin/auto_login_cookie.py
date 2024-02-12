# coding: utf-8
# ----------------------------------------------------------------------------------
# 非同期処理 自動ログインクラス
# headlessモード、reCAPTCHA回避、エラー時のみ通知（ライン、ChatWork、Slack）
# 2023/2/9制作

#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager

#---流れ--
# seleniumは非同期処理できない
# ----------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import pickle
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
import datetime

# モジュール
from logger.debug_logger import Logger
from autologin.solve_recaptcha import SolverRecaptcha
from notify.notify_line import LineNotify
from notify.notify_chatwork import ChatworkNotify
from notify.notify_slack import SlackNotify

load_dotenv()

executor = ThreadPoolExecutor(max_workers=5)

class AutoLogin:
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


        # SolverRecaptchaクラスを初期化
        self.recaptcha_solver = SolverRecaptcha(self.chrome)

        # LineNotifyクラスを初期化
        self.line_notify = LineNotify()

        # ChatworkNotifyクラスを初期化
        self.chatwork_notify = ChatworkNotify()

        # SlackNotifyクラスを初期化
        self.slack_notify = SlackNotify()



    # 同期的なログイン
    def auto_login(self, site_name, login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath, remember_box_xpath, cookies_file_name):
        self.logger.info(f"{site_name} Cookie作成を開始")
        self.chrome.get(login_url)

        # 現在のURL
        current_url = self.chrome.current_url
        self.logger.debug(current_url)



        # userid_xpathが出てくるまで待機
        try:
            WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located((By.XPATH, userid_xpath)))
            self.logger.debug(f"{site_name} 入力開始")
        
        except TimeoutException as e:
            print(f"タイムアウトエラー:{e}")

        # IDとパスを入力
        try:
            userid_field = self.chrome.find_element_by_xpath(userid_xpath)
            userid_field.send_keys(userid)
            self.logger.debug(f"{site_name} ID入力完了")

            password_field = self.chrome.find_element_by_xpath(password_xpath)
            password_field.send_keys(password)
            self.logger.debug(f"{site_name} パスワード入力完了")

        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")


        # ページが完全に読み込まれるまで待機
        WebDriverWait(self.chrome, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("ページは完全に表示されてる")


        WebDriverWait(self.chrome, 10).until(
            EC.visibility_of_element_located((By.XPATH, login_button_xpath))
        )
        self.logger.debug(f"{site_name} ボタンDOMの読み込みは完了してる")

        try:
            # ログインを維持するチェックボックスを探す
            remember_box = self.chrome.find_element_by_xpath(remember_box_xpath)
            self.logger.debug(f"{site_name} チェックボタンが見つかりました。")

        except ElementNotInteractableException as e:
            self.logger.error(f"{site_name} チェックボックスが見つかりません。{e}")

        except InvalidSelectorException:
            self.logger.debug(f"{site_name} チェックボックスないためスキップ")

        try:
            if remember_box:
            # remember_boxをクリックする
                remember_box.click()
            self.logger.debug(f"{site_name} チェックボタンをクリック")

        except UnboundLocalError:
            self.logger.debug(f"{site_name} チェックボタンなし")

        time.sleep(1)

        # reCAPTCHA検知
        try:
            # sitekeyを検索
            elements = self.chrome.find_elements_by_css_selector('[data-sitekey]')
            if len(elements) > 0:
                self.logger.info(f"{site_name} reCAPTCHA処理実施中")


                # solveRecaptchaファイルを実行
                try:
                    self.recaptcha_solver.handle_recaptcha(current_url)
                    self.logger.info(f"{site_name} reCAPTCHA処理、完了")

                except Exception as e:
                    self.logger.error(f"{site_name} reCAPTCHA処理に失敗しました")
                    # ログイン失敗をライン通知
                    self.line_notify.line_notify(f"{site_name} ログインが正しくできませんでした")


                self.logger.debug(f"{site_name} クリック開始")

                # ログインボタン要素を見つける
                login_button = self.chrome.find_element_by_id(f"{site_name} recaptcha-submit")

                # ボタンが無効化されているか確認し、無効化されていれば有効にする
                self.chrome.execute_script("document.getElementById('recaptcha-submit').disabled = false;")

                # ボタンをクリックする
                login_button.click()

            else:
                self.logger.info(f"{site_name} reCAPTCHAなし")

                login_button = self.chrome.find_element_by_xpath(login_button_xpath)
                self.logger.debug(f"{site_name} ボタン捜索完了")

                login_button.send_keys(Keys.ENTER)
                self.logger.debug(f"{site_name} クリック完了")


        # recaptchaなし
        except NoSuchElementException:
            self.logger.info(f"{site_name} reCAPTCHAなし")

            login_button = self.chrome.find_element_by_xpath(login_button_xpath)
            self.logger.debug(f"{site_name} ボタン捜索完了")

            try:
                login_button.send_keys(Keys.ENTER)
                self.logger.debug(f"{site_name} クリック完了")

            except ElementNotInteractableException:
                self.chrome.execute_script("arguments[0].click();", login_button)
                self.logger.debug(f"{site_name} JavaScriptを使用してクリック実行")


        # ページ読み込み待機
        try:
            # ログインした後のページ読み込みの完了確認
            WebDriverWait(self.chrome, 5).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.debug(f"{site_name} ログインページ読み込み完了")


        except Exception as e:
            self.logger.error(f"{site_name} handle_recaptcha を実行中にエラーが発生しました: {e}")




        # ログイン完了確認
        try:
            self.chrome.find_element_by_xpath(cart_element_xpath)
            self.logger.info(f"{site_name} ログイン完了")
            # self.chatwork_notify.chatwork_notify("ログインに成功")

            timestamp = 1742074325
            expiry_date = datetime.datetime.utcfromtimestamp(timestamp)
            print(expiry_date)

            # Cookieを取得する
            cookies = self.chrome.get_cookies()
            self.logger.debug(f"{site_name} Cookieの取得完了")

            # クッキーの存在を確認
            if cookies:
                self.logger.debug(f"{site_name} クッキーが存在します。")
                # for cookie in cookies:
                #     self.logger.debug(cookie)  # クッキーの詳細を表示
            else:
                self.logger.debug(f"{site_name} クッキーが存在しません。")

            # Cookieをscraper.subに保存する
            pickle.dump(cookies,open('/Users/nyanyacyan/Desktop/ProgramFile/project_file/shopers_scraping/scraper/scraper_subclass/cookies/' + cookies_file_name, 'wb'))
            self.logger.debug(f"{site_name} Cookieの保存完了")

        except NoSuchElementException:
            self.logger.error(f"{site_name} カートの確認が取れませんでした")
            # self.chatwork_notify.chatwork_image_notify("ログインに失敗。")
            # self.line_notify.line_image_notify("ログインに失敗。")
            # self.slack_notify.slack_image_notify("ログインに失敗。")

        time.sleep(1)

        self.logger.info(f"{site_name} Cookie作成、完了")

    # 同期メソッドを非同期処理に変換
    async def auto_login_async(self, site_name, login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath, remember_box_xpath, cookies_file_name):
        loop = asyncio.get_running_loop()

        # ブロッキング、実行タイミング、並列処理などを適切に行えるように「functools」にてワンクッション置いて実行
        await loop.run_in_executor(executor, functools.partial(self.auto_login, site_name, login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath, remember_box_xpath, cookies_file_name))