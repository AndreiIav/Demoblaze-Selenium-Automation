import allure
import pytest
from pages.products_page import ProductsPage


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_all_cards_are_visible_on_start_page in {browser_name}")
def test_all_cards_are_visible_on_start_page(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    all_cards = products_page.get_all_cards_on_page()

    assert len(all_cards) == 9


expected_product_type_with_app_category_button = [
    ("phone", "phones"),
    ("laptop", "laptops"),
    ("monitor", "monitors"),
]


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title(
    "test_expected_products_are_displayed_with_all_expected_details in {browser_name}"
)
@pytest.mark.parametrize(
    "expected_product_type_and_category", expected_product_type_with_app_category_button
)
def test_expected_products_are_displayed_with_all_expected_details(
    test_driver, base_url, get_products_json_data, expected_product_type_and_category
):
    expected_product_type, category_button = expected_product_type_and_category
    expected_products = get_products_json_data[expected_product_type]
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    products_page.click_categories_button(category_button=category_button)
    product_cards = products_page.get_all_product_cards()

    assert len(product_cards) == len(expected_products)
    for card in product_cards:
        for expected_product in expected_products:
            if card.title == expected_product.name:
                assert card.image_link == expected_product.link
                assert card.title_link == expected_product.link
                assert card.price == expected_product.price
                assert card.description == expected_product.description
