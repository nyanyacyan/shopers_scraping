# coding: utf-8
# ----------------------------------------------------------------------------------
# recaptcha回避　クラス
# 2023/1/20制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager


#---流れ--
# ２captchaからトークン取得→ トークンをtextareaに入力→ ログイン
# ----------------------------------------------------------------------------------
import sys
import os
from selenium.common.exceptions import NoSuchElementException

from twocaptcha import TwoCaptcha
from notify.notify_line import LineNotify
from dotenv import load_dotenv

# 自作モジュール
from logger.debug_logger import Logger

load_dotenv()

class SolverRecaptcha:
    def __init__(self, chrome_driver, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


        load_dotenv()
        self.line_notify = LineNotify()
        self.chrome = chrome_driver

        # 2captcha APIkeyを.envから取得
        self.api_key = os.getenv('APIKEY_2CAPTCHA')


    def solveRecaptcha(self, sitekey, url):
        solver = TwoCaptcha(self.api_key)

        try:
            result = solver.recaptcha(
                sitekey=sitekey,
                url=url)

        except Exception as e:
            sys.exit(e)

        else:
            return result
        



    def handle_recaptcha(self, current_url):
        try:
            self.logger.debug("display:noneを削除開始")

            # display:noneを[""](空欄)に書き換え
            self.chrome.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

            # 現在のdisplayプロパティ内の値を抽出
            style = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").style.display')

            self.logger.debug(style)

            if style == "":
                self.logger.debug("display:noneの削除に成功しました")
            else:
                raise Exception("display:noneの削除に失敗しました")

        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")

        except Exception as e:
            self.logger.error(f"display:noneの削除に失敗しましたので確認が必要です:{e}")
            self.line_notify.line_notify(f"{e}:詳細はログにてご確認ください")
            sys.exit(1)


        # data-sitekeyを検索
        recaptcha_element = self.chrome.find_element_by_css_selector('[data-sitekey]')

        # sitekeyの値を抽出
        data_sitekey_value = recaptcha_element.get_attribute('data-sitekey')

        self.logger.debug(f"data_sitekey_value: {data_sitekey_value}")
        self.logger.debug(f"current_url: {current_url}")

        self.logger.info("2captcha開始")

        result = self.solveRecaptcha(
            data_sitekey_value,
            current_url
        )

        try:
            # レスポンスがあった中のトークン部分を抽出
            code = result['code']

        except Exception as e:
            self.logger.error(f"エラーが発生しました: {e}")


        try:
            # トークンをtextareaに入力
            textarea = self.chrome.find_element_by_id('g-recaptcha-response')
            self.chrome.execute_script(f'arguments[0].value = "{code}";', textarea)

            # textareaの値を取得
            textarea_value = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").value;')

            if code == textarea_value:
                self.logger.debug("textareaにトークン入力完了")

        except Exception as e:
            self.logger.error(f"トークンの入力に失敗: {e}")
