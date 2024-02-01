# coding: utf-8
# ----------------------------------------------------------------------------------
# ライン通知　クラス
# 2023/1/26制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# requests==2.31.0
# pillow==10.2.0

# ----------------------------------------------------------------------------------

import os
import requests
from dotenv import load_dotenv

# モジュール
from logger.debug_logger import Logger

load_dotenv()
class LineNotify:
    def __init__(self):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


        # トークンを.envから取得
        # LINE通知したい人を選定してトークン作成=> .envに貼り付ける
        load_dotenv()
        self.line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')



    def line_notify(self, notification_message):
        """
        "Line Notify"からラインメッセージのみ通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}

        response = requests.post(line_notify_api, headers = headers, data=data)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")


    def line_image_notify(self, notification_message):
        """
        "Line Notify"からラインメッセージ + 画像通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}
        

        # 画像ファイルを指定する（png or jpeg）
        try:
            image_file = 'login_after_take.jpeg'
            with open(image_file, mode= 'rb') as jpeg_bin:
                files = {'imageFile': (image_file, jpeg_bin, 'image/jpeg')}
                response = requests.post(line_notify_api, headers = headers, data=data, files=files)

                if response.status_code == 200:
                    self.logger.debug("送信成功")
                else:
                    self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")

        except FileNotFoundError as e:
            self.logger.error(f"指定されてるファイルが見つかりません:{e}")
