# coding: utf-8
# ----------------------------------------------------------------------------------
# Tajimaya　自動ログイン
# 2023/1/20制作
# 仮想環境 / source autologin-v1/bin/activate
# reCAPTCHA有り


#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from autoLoginHeadless import AutoLogin


load_dotenv()  # .env ファイルから環境変数を読み込む
debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'  # 環境変数からデバッグモードを取得

# インスタンス作成
superdelivery_auto_login = AutoLogin(debug_mode=debug_mode)

# superdeliveryにログイン
superdelivery_auto_login.login(
    "https://www.tajimaya-oroshi.net/login.php",  # URL
    os.getenv('LOGIN_ID'),  # ID
    os.getenv('LOGIN_PASS'),  # password
    "//input[@name='loginEmail']",  # IDの検索する要素
    "//input[@name='loginPassword']",  # パスの検索する要素
    "//input[@type='submit']",  # クリックするボタン検索する要素
    "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"  # カートの有無でログイン確認
    )

