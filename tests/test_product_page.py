import pytest
from pages.product_page import ProductPage
from pages.products_page import ProductsPage

products_with_category = [
    ("Samsung galaxy s6", "phones"),
    ("2017 Dell 15.6 Inch", "laptops"),
    ("Apple monitor 24", "monitors"),
]


@pytest.mark.parametrize("products_and_category", products_with_category)
def test_product_details_match_card_details(
    test_driver, base_url, products_and_category
):
    product_name, product_category = products_and_category
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    test_driver.get(base_url)
    test_product_name = product_name

    products_page.click_categories_button(category_button=product_category)
    all_product_cards = products_page.get_all_product_cards()
    product_card = products_page.get_product_card(
        all_cards=all_product_cards, product_name=test_product_name
    )
    products_page.click_product_link(product_name=product_card.title)
    product_page_product = product_page.create_product()

    assert product_card.title == product_page_product.title
    assert product_card.price == product_page_product.price
    assert product_card.description == product_page_product.description


def test_add_product_to_cart(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    test_driver.get(base_url)
    test_product_name = "Samsung galaxy s6"

    products_page.click_categories_button(category_button="phones")
    products_page.click_product_link(product_name=test_product_name)

    product_page.click_add_to_cart_button()
    add_to_cart_alert_confirmation = product_page.ADD_TO_CART_ALERT_CONFIRMATION
    alert_text = product_page.get_alert_text()

    assert add_to_cart_alert_confirmation in alert_text
