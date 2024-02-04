import pytest
from unittest.mock import patch, MagicMock
from scraper_netsea import ScraperNetsea


@patch('selenium.webdriver.Chrome')
def test_scraper_netsea(mock_chrome):
    mock_driver_instance = MagicMock()
    mock_chrome.return_value = mock_driver_instance

    mock_element = MagicMock()
    mock_element.text = 'Test Price'
    mock_driver_instance.find_element_by_xpath.return_value = mock_element

    scraper = ScraperNetsea(chrome=mock_driver_instance, debug_mode=True)

    search_word = "test"
    scraper.scraper_netsea(search_word)

    mock_driver_instance.find_element_by_xpath.assert_any_call(scraper.netsea_search_field_xpath)
    mock_element.send_keys.assert_called_with(search_word)


    mock_driver_instance.find_element_by_xpath.assert_any_call(scraper.netsea_search_button_xpath)
    mock_search_button = mock_driver_instance.find_element_by_xpath.return_value
    mock_search_button.click.assert_called_once()

    # さらに、検索結果から特定の要素（例: 価格情報）が取得されたことを検証
    mock_driver_instance.find_element_by_xpath.assert_any_call(scraper.netsea_price_xpath)
