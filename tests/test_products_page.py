from pages.products_page import ProductsPage


def test_expected_phones_are_displayed(test_driver, base_url, get_products_json_data):
    expected_phones_products = get_products_json_data[0]
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    products_page.click_categories_button(category_button="phones")
    product_cards = products_page.get_product_cards()

    assert len(product_cards) == len(expected_phones_products)
    for i in range(len(product_cards)):
        assert product_cards[i].title == expected_phones_products[i].name
        assert product_cards[i].image_link == expected_phones_products[i].link
        assert product_cards[i].title_link == expected_phones_products[i].link
        assert product_cards[i].price == expected_phones_products[i].price
        assert product_cards[i].description == expected_phones_products[i].description


def test_expected_laptops_are_displayed(test_driver, base_url, get_products_json_data):
    expected_laptops_products = get_products_json_data[1]
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    products_page.click_categories_button(category_button="laptops")
    product_cards = products_page.get_product_cards()

    assert len(product_cards) == len(expected_laptops_products)
    for i in range(len(product_cards)):
        assert product_cards[i].title == expected_laptops_products[i].name
        assert product_cards[i].image_link == expected_laptops_products[i].link
        assert product_cards[i].title_link == expected_laptops_products[i].link
        assert product_cards[i].price == expected_laptops_products[i].price
        assert product_cards[i].description == expected_laptops_products[i].description


def test_expected_monitors_are_displayed(test_driver, base_url, get_products_json_data):
    expected_monitors_products = get_products_json_data[2]
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    products_page.click_categories_button(category_button="monitors")
    product_cards = products_page.get_product_cards()

    assert len(product_cards) == len(expected_monitors_products)
    for i in range(len(product_cards)):
        assert product_cards[i].title == expected_monitors_products[i].name
        assert product_cards[i].image_link == expected_monitors_products[i].link
        assert product_cards[i].title_link == expected_monitors_products[i].link
        assert product_cards[i].price == expected_monitors_products[i].price
        assert product_cards[i].description == expected_monitors_products[i].description


def test_categories_links(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    category_buttons = ("phones", "laptops", "monitors")

    for category_button in category_buttons:
        products_page.click_categories_button(category_button=category_button)


def test_all_cards_are_visible(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    all_cards = products_page.get_all_cards_on_page()

    assert len(all_cards) == 9


def test_card_links(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    all_image_links = products_page.get_all_cards_links(link_origin="card_image")

    assert len(all_image_links) == 9
    assert "https://www.demoblaze.com/prod.html?idp_=1" in all_image_links


def test_card_product_names(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    all_card_titles = products_page.get_all_cards_titles()

    assert len(all_card_titles) == 9
    assert "Samsung galaxy s6" in all_card_titles


def test_card_prices(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)

    all_cards_prices = products_page.get_all_cards_prices()

    assert len(all_cards_prices) == 9
    assert 360 in all_cards_prices


def test_card_descriptions(test_driver, base_url):
    products_page = ProductsPage(test_driver)
    test_driver.get(base_url)
    description = (
        "The Samsung Galaxy S6 is powered by 1.5GHz octa-core Samsung Exynos 7420 processor and it comes with 3GB of RAM. "
        "The phone packs 32GB of internal storage cannot be expanded."
    )

    all_cards_descriptions = products_page.get_all_cards_descriptions()

    assert len(all_cards_descriptions) == 9
    assert description in all_cards_descriptions
