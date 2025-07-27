import allure
import pytest
from flows.flows import ProductToCartFlow
from pages.cart_page import CartPage
from pages.navbar_page import NavbarPage
from pages.product_page import ProductPage
from pages.products_page import ProductsPage


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_product_is_displayed_in_products_table in {browser_name}")
def test_product_is_displayed_in_products_table(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    test_driver.get(base_url)
    product_to_cart_flow = ProductToCartFlow(
        product_page=product_page, products_page=products_page
    )
    test_product_name = "Samsung galaxy s6"
    test_product_category = "phones"
    test_product_link = "https://www.demoblaze.com/imgs/galaxy_s6.jpg"
    test_product_price = 360

    # add test product to cart
    product_to_cart_flow.add_product_to_cart(
        category_button=test_product_category, product_name=test_product_name
    )

    # go to Cart page
    navbar_page.click_navbar_button(button="cart")

    # check that the products table is displayed with the correct headers
    assert cart_page.get_product_table_header_text(header="picture") == "Pic"
    assert cart_page.get_product_table_header_text(header="title") == "Title"
    assert cart_page.get_product_table_header_text(header="price") == "Price"
    assert cart_page.get_product_table_header_text(header="delete") == "x"

    # check that test product is displayed in the table with correct details
    all_product_rows = cart_page.get_all_product_rows()
    product_rows_cards = cart_page.create_product_rows_cards(
        product_rows=all_product_rows
    )
    test_product = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=test_product_name
    )
    assert test_product.image_link == test_product_link
    assert test_product.title == test_product_name
    assert test_product.price == test_product_price


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_product_page_details_match_cart_page_details in {browser_name}")
def test_product_page_details_match_cart_page_details(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    product_to_cart_flow = ProductToCartFlow(
        product_page=product_page, products_page=products_page
    )
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    test_driver.get(base_url)
    phone_test_product_name = "Samsung galaxy s6"
    phone_test_product_category = "phones"
    laptop_test_product_name = "2017 Dell 15.6 Inch"
    laptop_test_product_category = "laptops"
    monitor_test_product_name = "Apple monitor 24"
    monitor_test_product_category = "monitors"

    # add test products to cart

    phone_product = product_to_cart_flow.add_product_to_cart_and_get_product(
        category_button=phone_test_product_category,
        product_name=phone_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    laptop_product = product_to_cart_flow.add_product_to_cart_and_get_product(
        category_button=laptop_test_product_category,
        product_name=laptop_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add monitor
    monitor_product = product_to_cart_flow.add_product_to_cart_and_get_product(
        category_button=monitor_test_product_category,
        product_name=monitor_test_product_name,
    )

    # go to Cart page
    navbar_page.click_navbar_button(button="cart")

    # get all products from products table
    product_rows = cart_page.get_all_product_rows()
    # create ProductRowsCards
    product_rows_cards = cart_page.create_product_rows_cards(product_rows=product_rows)
    phone_product_row = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=phone_test_product_name
    )
    laptop_product_row = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=laptop_test_product_name
    )
    monitor_product_row = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=monitor_test_product_name
    )

    assert phone_product.title == phone_product_row.title
    assert phone_product.price == phone_product_row.price

    assert laptop_product.title == laptop_product_row.title
    assert laptop_product.price == laptop_product_row.price

    assert monitor_product.title == monitor_product_row.title
    assert monitor_product.price == monitor_product_row.price


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_total_cart_price_matches_products_total_price in {browser_name}")
def test_total_cart_price_matches_products_total_price(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    product_to_cart_flow = ProductToCartFlow(
        product_page=product_page, products_page=products_page
    )
    test_driver.get(base_url)
    phone_test_product_name = "Samsung galaxy s6"
    phone_test_product_category = "phones"
    laptop_test_product_name = "2017 Dell 15.6 Inch"
    laptop_test_product_category = "laptops"
    monitor_test_product_name = "Apple monitor 24"
    monitor_test_product_category = "monitors"

    # add test products to cart

    # add phone
    product_to_cart_flow.add_product_to_cart(
        category_button=phone_test_product_category,
        product_name=phone_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add laptop
    product_to_cart_flow.add_product_to_cart(
        category_button=laptop_test_product_category,
        product_name=laptop_test_product_name,
    )
    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add monitor
    product_to_cart_flow.add_product_to_cart(
        category_button=monitor_test_product_category,
        product_name=monitor_test_product_name,
    )

    # go to Cart page
    navbar_page.click_navbar_button(button="cart")

    # get all products from products table
    product_rows = cart_page.get_all_product_rows()

    # create ProductRowsCards
    product_rows_cards = cart_page.create_product_rows_cards(product_rows=product_rows)

    total_products_table_price = sum(
        product_row.price for product_row in product_rows_cards
    )
    cart_total_price = cart_page.get_cart_total_price()

    assert total_products_table_price == cart_total_price


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_total_cart_price_drops_after_deleting_product in {browser_name}")
def test_total_cart_price_drops_after_deleting_product(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    test_driver.get(base_url)
    product_to_cart_flow = ProductToCartFlow(
        product_page=product_page, products_page=products_page
    )
    phone_test_product_name = "Samsung galaxy s6"
    phone_test_product_category = "phones"
    laptop_test_product_name = "2017 Dell 15.6 Inch"
    laptop_test_product_category = "laptops"
    monitor_test_product_name = "Apple monitor 24"
    monitor_test_product_category = "monitors"

    # add test products to cart

    # add phone
    product_to_cart_flow.add_product_to_cart(
        category_button=phone_test_product_category,
        product_name=phone_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add laptop
    product_to_cart_flow.add_product_to_cart(
        category_button=laptop_test_product_category,
        product_name=laptop_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add monitor
    product_to_cart_flow.add_product_to_cart(
        category_button=monitor_test_product_category,
        product_name=monitor_test_product_name,
    )

    # go to Cart page
    navbar_page.click_navbar_button(button="cart")

    # get all products from products table
    product_rows = cart_page.get_all_product_rows()
    # create ProductRowsCards
    product_rows_cards = cart_page.create_product_rows_cards(product_rows=product_rows)

    total_products_table_price = sum(
        product_row.price for product_row in product_rows_cards
    )
    cart_total_price = cart_page.get_cart_total_price()

    assert total_products_table_price == cart_total_price

    # delete product
    product_to_be_deleted = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=laptop_test_product_name
    )
    expected_cart_price_after_deleting_product = (
        cart_total_price - product_to_be_deleted.price
    )
    cart_page.delete_product(element=product_to_be_deleted.delete_button)

    # get all products from products table after deleting one product
    product_rows = cart_page.get_all_product_rows()
    product_rows_cards = cart_page.create_product_rows_cards(product_rows=product_rows)

    total_products_table_price = sum(
        product_row.price for product_row in product_rows_cards
    )
    cart_total_price_updated = cart_page.get_cart_total_price()

    assert total_products_table_price == cart_total_price_updated
    assert cart_total_price_updated == expected_cart_price_after_deleting_product


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
@allure.title("test_can_place_order_succesfully in {browser_name}")
def test_can_place_order_succesfully(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    product_to_cart_flow = ProductToCartFlow(
        product_page=product_page, products_page=products_page
    )
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    test_driver.get(base_url)

    phone_test_product_name = "Iphone 6 32gb"
    phone_test_product_category = "phones"
    laptop_test_product_name = "MacBook Pro"
    laptop_test_product_category = "laptops"
    monitor_test_product_name = "ASUS Full HD"
    monitor_test_product_category = "monitors"
    costumer_name = "John Doe"
    costumer_country = "Italy"
    costumer_city = "Rome"
    costumer_credit_card = "1234 brdc 9876"
    transaction_month = "6"
    transaction_year = "2025"
    expected_confirmation_message = "Thank you for your purchase!"
    expected_date = cart_page.create_confirmation_prompt_expected_date()

    # add test products to cart

    # add phone
    product_to_cart_flow.add_product_to_cart(
        category_button=phone_test_product_category,
        product_name=phone_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add laptop
    product_to_cart_flow.add_product_to_cart(
        category_button=laptop_test_product_category,
        product_name=laptop_test_product_name,
    )

    # go to Home page
    navbar_page.click_navbar_button(button="home")

    # add monitor
    product_to_cart_flow.add_product_to_cart(
        category_button=monitor_test_product_category,
        product_name=monitor_test_product_name,
    )

    # go to Cart page
    navbar_page.click_navbar_button(button="cart")

    # Fill Order details
    cart_page.get_place_order_modal()
    modal_cart_price = cart_page.get_modal_cart_price()
    cart_page.fill_place_order_modal_fields(
        name=costumer_name,
        country=costumer_country,
        city=costumer_city,
        credit_card=costumer_credit_card,
        month=transaction_month,
        year=transaction_year,
    )
    cart_page.purchase_order()

    confirmation_message = cart_page.get_confirmation_prompt_message()
    confirmation_prompt_data = cart_page.get_confirmation_data()
    cart_page.click_confirmation_prompt_ok_button()

    assert confirmation_message == expected_confirmation_message
    assert confirmation_prompt_data.order_id_numeric > 0
    assert (
        confirmation_prompt_data.order_amount == f"Amount: {int(modal_cart_price)} USD"
    )
    assert (
        confirmation_prompt_data.card_number == f"Card Number: {costumer_credit_card}"
    )
    assert confirmation_prompt_data.name == f"Name: {costumer_name}"
    assert confirmation_prompt_data.order_date == expected_date
