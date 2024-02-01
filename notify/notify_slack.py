# coding: utf-8
# ----------------------------------------------------------------------------------
# Slack通知　クラス
# 2023/1/28制作
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
class SlackNotify:
    def __init__(self):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


        # トークンを.envから取得
        # 通知するチャンネルから権限を選択=> アプリインストールしてトークン作成=> .envに貼り付ける
        # slackの場合、メッセージ+画像はNG。画像+コメントになる
        load_dotenv()
        self.slack_notify_token = os.getenv('SLACK_NOTIFY_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL')



    def slack_notify(self, notification_message):
        """
        "Slack Notify"からラインメッセージのみ通知する
        """
        slack_notify_api = 'https://slack.com/api/chat.postMessage'
        headers = {'Authorization': f'Bearer {self.slack_notify_token}'}
        data = {
            'channel': {self.slack_channel},
            'text': {notification_message}
        }

        response = requests.post(slack_notify_api, headers = headers, data=data)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")


    def slack_image_notify(self, notification_message):
        """
        "Slack Notify"から 画像 + コメント 通知する
        """


        slack_files_upload_api = 'https://slack.com/api/files.upload'
        headers = {'Authorization': f'Bearer {self.slack_notify_token}'}
        data = {
            'channels': self.slack_channel,
            'initial_comment': notification_message,
            'filename': 'login_after_take.jpeg'
        }

        # 画像ファイルを指定する（png or jpeg）
        try:
            image_file = 'login_after_take.jpeg'
            with open(image_file, 'rb') as jpeg_bin:
                files = {'file': (image_file, jpeg_bin, 'image/jpeg')}
                
                # Slackに画像とメッセージを送る
                response = requests.post(slack_files_upload_api, headers = headers, data=data, files=files)

                if response.status_code == 200:
                    self.logger.debug("送信成功")
                else:
                    self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")

        except FileNotFoundError as e:
            self.logger.error(f"指定されてるファイルが見つかりません:{e}")







