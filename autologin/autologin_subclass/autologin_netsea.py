# coding: utf-8
# ----------------------------------------------------------------------------------
# netsea自動ログイン
# 2023/1/20制作
# source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager


#---流れ--
# ID入力=> パス入力=> クリック
# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from autoLoginHeadless import AutoLogin


load_dotenv()  # .env ファイルから環境変数を読み込む
debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'  # 環境変数からデバッグモードを取得

# インスタンス作成
netsea_auto_login = AutoLogin(debug_mode=debug_mode)

# netseaにログイン
netsea_auto_login.login(
    "https://www.netsea.jp/login",  # URL
    os.getenv('LOGIN_ID'),  # ID
    os.getenv('LOGIN_PASS'),  # password
    "//input[@name='login_id']",  # IDの検索する要素
    "//input[@name='password']",  # パスの検索する要素
    "//button[@name='submit']",  # クリックするボタン検索する要素
    "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # カートの有無でログイン確認
    )

