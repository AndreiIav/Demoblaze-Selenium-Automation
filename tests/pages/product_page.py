from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


@dataclass
class Product:
    """Represents a product with all its details"""

    title: str
    price: float
    description: str


class ProductPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, "#tbodyid > .name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "#tbodyid > .price-container")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "#more-information p")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a.btn")
    ADD_TO_CART_ALERT_CONFIRMATION = "Product added"

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_product_name(self) -> str:
        product_name = self.get_element_text(locator=self.PRODUCT_NAME)
        return product_name

    def get_product_price(self) -> float:
        product_price = self.get_element(locator=self.PRODUCT_PRICE)

        # product_price is a string like '$360 *includes tax'
        # remove '$' and' *includes tax' from the price string and convert
        # the price to a float
        price = float(product_price.text[1:-14])
        return price

    def get_product_description(self) -> str:
        product_description = self.get_element_text(locator=self.PRODUCT_DESCRIPTION)
        return product_description

    def click_add_to_cart_button(self) -> None:
        self.click_button(locator=self.ADD_TO_CART_BUTTON)

    def create_product(self) -> Product:
        """Creates Product objects"""

        new_product = Product(
            title=self.get_product_name(),
            price=self.get_product_price(),
            description=self.get_product_description(),
        )

        return new_product
