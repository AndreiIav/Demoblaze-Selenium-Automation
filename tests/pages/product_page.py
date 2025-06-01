from dataclasses import dataclass

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, "#tbodyid > .name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "#tbodyid > .price-container")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "#more-information p")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '[onclick="addToCart(1)"]')
    ADD_TO_CART_ALERT_CONFIRMATION = "Product added"

    def __init__(self, driver):
        super().__init__(driver)

    @dataclass
    class Product:
        """Represents a product with all its details"""

        title: str
        price: float
        description: str

    def get_product_name(self):
        product_name = self.get_element_text(locator=self.PRODUCT_NAME)
        return product_name

    def get_product_price(self):
        product_price = self.get_element(locator=self.PRODUCT_PRICE)

        # product_price is a string like '$360 *includes tax'
        # remove '$' and' *includes tax' from the price string and convert
        # the price to a float
        price = float(product_price.text[1:-14])
        return price

    def get_product_description(self):
        product_description = self.get_element_text(locator=self.PRODUCT_DESCRIPTION)
        return product_description

    def click_add_to_cart_button(self):
        add_to_cart_button = self.get_element(self.ADD_TO_CART_BUTTON)
        add_to_cart_button.click()

    def create_product(self):
        """Creates Product objects"""

        new_product = self.Product(
            title=self.get_product_name(),
            price=self.get_product_price(),
            description=self.get_product_description(),
        )

        return new_product
