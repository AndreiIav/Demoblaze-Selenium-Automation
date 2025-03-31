from collections import namedtuple

import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        help="Browser to run tests (chrome/firefox)",
        choices=("chrome", "firefox"),
    )

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
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def is_headeless(request):
    return request.config.getoption("--headless")


@pytest.fixture
def browser_option(browser_name, is_headeless):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if is_headeless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return options

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if is_headeless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        return options


@pytest.fixture()
def test_driver(browser_name, browser_option, run_on_selenium_grid):
    if run_on_selenium_grid:
        if browser_name == "chrome":
            driver = webdriver.Remote("http://localhost:4444", options=browser_option)
        elif browser_name == "firefox":
            driver = webdriver.Remote("http://localhost:4444", options=browser_option)
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


@pytest.fixture()
def user_credentials():
    User = namedtuple("User", ["username", "password"])
    user = User(username="abc_12", password="abc")
    return user


@pytest.fixture()
def base_url():
    base_url = "https://www.demoblaze.com/"
    return base_url
