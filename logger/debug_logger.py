# coding: utf-8
# ----------------------------------------------------------------------------------
# recaptchaProcessクラス
# 2023/1/20制作
# source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import logging
import os

class LoggerBasicColor(logging.Formatter):
    COLORS = {
        "INFO": "\033[94m",  # 青色
        "ERROR" : "\033[91m",
    }

    RESET = "\033[0m"

    def format(self, record):
        message = super().format(record)
        color = self.COLORS.get(record.levelname, "")
        return f"{color}{message}{self.RESET}"

class Logger:
    def __init__(self, module_name, debug_mode=False):
        try:
            self.logger = logging.getLogger(module_name)

            # 同じログは表示しないように設定
            if not self.logger.handlers:
                self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

                # コンソールにログを出力するハンドラを追加
                console_handler = logging.StreamHandler()
                self.logger.addHandler(console_handler)

                # ログのフォーマットを設定
                log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                console_handler.setFormatter(log_format)

                log_format = LoggerBasicColor('%(asctime)s - %(levelname)s - %(message)s')
                console_handler.setFormatter(log_format)

                # ログファイルの保存先ディレクトリを設定
                log_directory = "logs"

                # 各モジュールの名前でログファイルを分ける
                log_filename = f"{log_directory}/{module_name}_debug.log"

                # ディレクトリが存在しない場合は作成
                if not os.path.exists(log_directory):
                    os.makedirs(log_directory)

                # ファイル出力用のハンドラー
                file_handler = logging.FileHandler(log_filename)  # ファイル名を指定
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

        except Exception as e:
            print(f"ロガー設定中にエラーが発生しました: {e}")


    def get_logger(self):
        return self.logger