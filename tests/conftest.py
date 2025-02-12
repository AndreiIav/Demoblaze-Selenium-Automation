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
def test_driver(browser_name, browser_option):
    if browser_name == "chrome":
        driver = webdriver.Chrome(options=browser_option)
    elif browser_name == "firefox":
        driver = webdriver.Firefox(options=browser_option)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver

    driver.quit()
