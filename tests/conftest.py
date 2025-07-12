import json
import os
from collections import namedtuple
from dataclasses import dataclass

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
def is_headless(request):
    return request.config.getoption("--headless")


@pytest.fixture
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


@pytest.fixture()
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


@pytest.fixture()
def user_credentials():
    User = namedtuple("User", ["username", "password"])
    user = User(username="abc_12", password="abc")
    return user


@pytest.fixture()
def base_url():
    base_url = "https://www.demoblaze.com/"
    return base_url


@dataclass
class Product:
    category: str
    name: str
    link: str
    price: float
    description: str


def get_json_data(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    return data


@pytest.fixture
def get_products_json_data():
    expected_products = get_json_data(json_file="tests/products.json")
    expected_products_data = {"phone": [], "laptop": [], "monitor": []}

    for expected_product_name in expected_products_data:
        category_products = {
            name: details
            for name, details in expected_products.items()
            if details["category"] == expected_product_name
        }

        for name, value in category_products.items():
            prod = Product(
                category=value["category"],
                name=name,
                link=value["link"],
                price=value["price"],
                description=value["description"],
            )
            expected_products_data[expected_product_name].append(prod)

    return expected_products_data
