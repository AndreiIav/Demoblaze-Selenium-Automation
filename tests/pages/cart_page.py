from dataclasses import dataclass

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class CartPage(BasePage):
    # Products table
    PRODUCT_TABLE_HEADER_PIC = (
        By.CSS_SELECTOR,
        ".table > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1)",
    )
    PRODUCT_TABLE_HEADER_TITLE = (
        By.CSS_SELECTOR,
        ".table > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(2)",
    )
    PRODUCT_TABLE_HEADER_PRICE = (
        By.CSS_SELECTOR,
        ".table > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(3)",
    )
    PRODUCT_TABLE_HEADER_DELETE = (
        By.CSS_SELECTOR,
        ".table > thead:nth-child(1) > tr:nth-child(1) > th:nth-child(4)",
    )
    PRODUCT_TABLE_PRODUCT_ROW = (By.CSS_SELECTOR, "tr.success")
    PRODUCT_TABLE_PRODUCT_PIC = (By.CSS_SELECTOR, "td:nth-child(1) > img:nth-child(1)")
    PRODUCT_TABLE_PRODUCT_TITLE = (By.CSS_SELECTOR, "td:nth-child(2)")
    PRODUCT_TABLE_PRODUCT_PRICE = (By.CSS_SELECTOR, "td:nth-child(3)")
    PRODUCT_TABLE_PRODUCT_DELETE = (By.CSS_SELECTOR, "td:nth-child(4) > a:nth-child(1)")

    # Total and Place Order
    CART_TOTAL_VALUE = (By.ID, "totalp")

    @dataclass
    class ProductRowCard:
        """Represents a product row with all its details"""

        image_link: str
        title: str
        price: float
        delete_button: WebElement

    def get_product_table_header_text(self, header):
        if header == "picture":
            header_selector = self.PRODUCT_TABLE_HEADER_PIC
        elif header == "title":
            header_selector = self.PRODUCT_TABLE_HEADER_TITLE
        elif header == "price":
            header_selector = self.PRODUCT_TABLE_HEADER_PRICE
        elif header == "delete":
            header_selector = self.PRODUCT_TABLE_HEADER_DELETE

        product_table_header_text = self.get_element_text(locator=header_selector)
        return product_table_header_text

    def get_all_product_rows(self):
        product_rows = self.get_all_elements(locator=self.PRODUCT_TABLE_PRODUCT_ROW)
        return product_rows

    def get_product_row_image_link(self, product_row):
        image_link = (
            self.get_sub_element_attribute(
                parent_element=product_row,
                locator=self.PRODUCT_TABLE_PRODUCT_PIC,
                attribute="src",
            ),
        )
        return image_link[0]

    def get_product_row_title(self, product_row):
        product_title = self.get_sub_element_text(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_TITLE
        )
        return product_title

    def get_product_row_price(self, product_row):
        product_price = self.get_sub_element_text(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_PRICE
        )
        return float(product_price)

    def get_product_row_delete_button(self, product_row):
        element = self.get_sub_element(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_DELETE
        )
        return element

    def create_product_rows_cards(self, product_rows):
        product_rows_cards = []

        for product_row in product_rows:
            new_product_row_card = self.ProductRowCard(
                image_link=self.get_product_row_image_link(product_row=product_row),
                title=self.get_product_row_title(product_row=product_row),
                price=self.get_product_row_price(product_row=product_row),
                delete_button=self.get_product_row_delete_button(
                    product_row=product_row
                ),
            )

            product_rows_cards.append(new_product_row_card)

        return product_rows_cards

    def get_product_card(self, all_cards, product_name):
        """
        Returns a single ProductCard object or raises a LookupError if the name
        is not found.

        Args:
            all_cards (list): A list of ProductCard objects.
            product_name (str): The name of the product to be returned.
        """
        try:
            card = next(c for c in all_cards if c.title == product_name)
            return card
        except StopIteration:
            raise LookupError(
                f"'{product_name}' product can not be found in all_cards."
            )

    def click_product_delete_button(self, product_card):
        product_delete_button = self.get_clickabale_element(
            locator=product_card.delete_button
        )
        product_delete_button.click()

    def get_cart_total_value(self):
        cart_total_value = self.get_element_text(locator=self.CART_TOTAL_VALUE)
        return float(cart_total_value)
