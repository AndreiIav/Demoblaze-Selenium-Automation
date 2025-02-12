import pytest
from selenium import webdriver


@pytest.fixture()
def firefox_browser():
    driver = webdriver.Firefox()

    yield driver

    driver.quit()
