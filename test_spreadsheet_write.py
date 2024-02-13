import asyncio
from spreadsheet.price_url_write import SpreadsheetWrite  # 'spreadsheet_write'はSpreadsheetWriteクラスが定義されているファイル名に置き換えてください

async def test_spreadsheet_write():
    sw = SpreadsheetWrite(debug_mode=True)
    await sw.spreadsheet_write()

if __name__ == "__main__":
    asyncio.run(test_spreadsheet_write())