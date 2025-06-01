from pages.cart_page import CartPage
from pages.navbar_page import NavbarPage
from pages.product_page import ProductPage
from pages.products_page import ProductsPage


def test_product_is_displayed_in_products_table(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    product_page = ProductPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    cart_page = CartPage(test_driver)
    test_driver.get(base_url)
    test_product_name = "Samsung galaxy s6"

    # add test product to cart
    products_page.click_categories_button(category_button="phones")
    products_page.click_product_link(product_name=test_product_name)
    product_page.click_add_to_cart_button()
    product_page.get_alert_text()
    product_page.accept_alert()

    # go to Cart page
    navbar_page.click_button(button="cart")

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
    assert (
        product_rows_cards[0].image_link
        == "https://www.demoblaze.com/imgs/galaxy_s6.jpg"
    )
    assert product_rows_cards[0].title == "Samsung galaxy s6"
    assert product_rows_cards[0].price == 360

    # check if cart total value matches the product's value
    cart_total_value = cart_page.get_cart_total_value()
    assert product_rows_cards[0].price == cart_total_value

    # delete product
    product_row = cart_page.get_product_card(
        all_cards=product_rows_cards, product_name=test_product_name
    )
    cart_page.click_product_delete_button(product_card=product_row)
