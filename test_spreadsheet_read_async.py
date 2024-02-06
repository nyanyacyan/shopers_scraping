import asyncio
import datetime
from process import Process

async def test_spreadsheet_read_async():
    print(f"開始時刻: {datetime.datetime.now()}")
    # Processクラスのインスタンスを生成
    process_instance = Process(chrome=None)  # ここでは例示のためNoneを渡しています。

    # スプレッドシートからのデータ読み込みを非同期で実行
    dic_data = await process_instance.spreadsheet_read_async_instance.spreadsheet_read_async()
    print(f"終了時刻: {datetime.datetime.now()}")
    print(f"スプシ記載されたJAN、商品名: {dic_data}")

if __name__ == "__main__":
    asyncio.run(test_spreadsheet_read_async())
