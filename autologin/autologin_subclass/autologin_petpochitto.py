# coding: utf-8
# ----------------------------------------------------------------------------------
# PETポチッと　自動ログイン
# 2023/1/20制作

#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
from dotenv import load_dotenv
import os
from autoLoginHeadless import AutoLogin


load_dotenv()  # .env ファイルから環境変数を読み込む
debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'  # 環境変数からデバッグモードを取得

# インスタンス作成
petpochitto_auto_login = AutoLogin(debug_mode=debug_mode)

# petpochittoにログイン
petpochitto_auto_login.login(
    "https://www.petpochitto.com/login.php",  # URL
    os.getenv('LOGIN_ID'),  # ID
    os.getenv('LOGIN_PASS'),  # password
    "//input[@name='loginEmail']",  # IDの検索する要素
    "//input[@name='loginPassword']",  # パスの検索する要素
    "//input[@name='login']",  # クリックするボタン検索する要素
    "//img[contains(@src, 'cart') and contains(@alt, '買い物カゴ')]"  # カートの有無でログイン確認
    )
