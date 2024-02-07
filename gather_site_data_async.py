import asyncio
from auto_scraper_oroshiuri import AutoScraperOroshiuri  # 自作クラスのインポートパスを適宜調整してください
from auto_scraper_netsea import AutoScraperNetsea

async def gather_site_data_async():
    # 各クラスのインスタンスを作成
    netsea_scraper = AutoScraperNetsea(debug_mode=True)
    oroshiuri_scraper = AutoScraperOroshiuri(debug_mode=True)

    # 並列処理を実施して、それぞれの変数に代入
    netsea_result, oroshiuri_result = await asyncio.gather(
        netsea_scraper.auto_scraper_netsea_async(),
        oroshiuri_scraper.auto_scraper_oroshiuri_async()
    )

    # 各結果をresultsに追加
    results = []
    results.append(netsea_result)  # netsea_result をリストに追加
    results.append(oroshiuri_result) 

    # 結果を表示
    print(f"スクレイピング結果:{results}")

    return results