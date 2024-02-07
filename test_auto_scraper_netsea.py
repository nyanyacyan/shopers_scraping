import asyncio
from auto_scraper_netsea import AutoScraperNetsea  # 自作クラスのインポートパスを適宜調整してください

async def test_auto_scraper_netsea():
    # AutoScraperNetsea クラスのインスタンスを作成
    scraper = AutoScraperNetsea(debug_mode=True)

    # スクレイピングメソッドを非同期で実行
    result = await scraper.auto_scraper_netsea_async()

    # 結果を表示
    print(f"スクレイピング結果:{result}")

    # ここで結果を検証し、期待通りであることを確認する
    # 例: assert文を使用して結果が期待値と一致することを確認する（実際のテストケースに応じて調整）
    # assert result == expected_value

if __name__ == "__main__":
    asyncio.run(test_auto_scraper_netsea())
