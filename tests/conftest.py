import os
from collections import namedtuple

import pytest
from selenium import webdriver
from utils.data_loader import parse_products_json_data


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", help="Run browser in headless mode"
    )

    parser.addoption(
        "--selenium_grid", action="store_true", help="Run tests on Selenium Grid"
    )


@pytest.fixture(scope="session")
def run_on_selenium_grid(request):
    return request.config.getoption("--selenium_grid")


@pytest.fixture(scope="session")
def is_headless(request):
    return request.config.getoption("--headless")


@pytest.fixture(scope="function")
def browser_option(browser_name, is_headless):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return options

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if is_headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        return options


@pytest.fixture(scope="function")
def test_driver(browser_name, browser_option, run_on_selenium_grid):
    if run_on_selenium_grid:
        if browser_name in ("chrome", "firefox"):
            command_executor = os.getenv(
                "SELENIUM_HUB_URL", default="http://localhost:4444"
            )
            driver = webdriver.Remote(
                command_executor=command_executor,
                options=browser_option,
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    else:
        if browser_name == "chrome":
            driver = webdriver.Chrome(options=browser_option)
        elif browser_name == "firefox":
            driver = webdriver.Firefox(options=browser_option)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def user_credentials():
    User = namedtuple("User", ["username", "password"])
    user = User(username="abc_12", password="abc")
    return user


@pytest.fixture(scope="session")
def base_url():
    base_url = "https://www.demoblaze.com/"
    return base_url


@pytest.fixture(scope="session")
def expected_products():
    expected_products_data = parse_products_json_data()
    return expected_products_data
