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

    def get_product_name(self):
        self.is_element_visible(self.PRODUCT_NAME)
        product_name = self.driver.find_element(*self.PRODUCT_NAME)
        return product_name.text

    def get_product_price(self):
        self.is_element_visible(self.PRODUCT_PRICE)
        product_price = self.driver.find_element(*self.PRODUCT_PRICE)

        # product_price is a string like '$360 *includes tax'
        # remove '$' and' *includes tax' from the price string and convert
        # the price to a float
        price = float(product_price.text[1:-14])
        return price

    def get_product_description(self):
        self.is_element_visible(self.PRODUCT_DESCRIPTION)
        product_description = self.driver.find_element(*self.PRODUCT_DESCRIPTION)
        return product_description.text

    def click_add_to_cart_button(self):
        self.is_element_visible(self.ADD_TO_CART_BUTTON)
        add_to_cart_button = self.driver.find_element(*self.ADD_TO_CART_BUTTON)
        add_to_cart_button.click()

    def get_alert_text(self):
        alert = self.get_alert()
        alert_text = alert.text
        return alert_text

    def accept_alert(self):
        alert = self.get_alert()
        alert.accept()
