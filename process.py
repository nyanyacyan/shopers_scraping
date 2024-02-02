from autologin.autologin_subclass.auto_login_netsea import AutoLoginNetsea
from autologin.autologin_subclass.auto_login_oroshiuri import AutoLoginOroshiuri
from autologin.autologin_subclass.auto_login_petpochitto import AutoLoginPetpochitto
from autologin.autologin_subclass.auto_login_superdelivery import AutoLoginSuperDelivery
from autologin.autologin_subclass.auto_login_tajimaya import AutoLoginTajimaya

from scraper.scraper_subclass.scraper_netsea import ScraperNetsea
from scraper.scraper_subclass.scraper_oroshiuri import ScraperOroshiuri
from scraper.scraper_subclass.scraper_petpochitto import ScraperPetpochitto
from scraper.scraper_subclass.scraper_super_delivery import ScraperSuperDelivery
from scraper.scraper_subclass.scraper_tajimaya import ScraperTajimaya

from spreadsheet.read import Spreadsheet_read
from spreadsheet.write import Spreadsheet_write

from logger.debug_logger import Logger

def process_scraper_netsea():
    data = Spreadsheet_read.spreadsheet_read()
    Logger.debug(f"スプシ記載されたJAN、商品名: {data}")

    # Logger.debug("netseaオートログインスタート")
    # AutoLoginNetsea.auto_login_netsea()
    # Logger.debug("netseaオートログイン完了")

    # Logger.debug("netseaスクレイピングスタート")
    # ScraperNetsea.scraper_netsea()
    # Logger.debug("netseaスクレイピング終了")

    return data