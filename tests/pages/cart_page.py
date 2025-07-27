from dataclasses import dataclass
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


@dataclass
class ProductRowCard:
    """Represents a product row with all its details"""

    image_link: str
    title: str
    price: float
    delete_button: WebElement


@dataclass
class ConfirmationPromptData:
    """Represents the confirmation prompt details for an order"""

    order_id_raw: str
    # store the numerical part of id
    order_id_numeric: int
    order_amount: str
    card_number: str
    name: str
    order_date: str


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
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button.btn:nth-child(3)")

    # Place Order Modal
    PLACE_ORDER_MODAL = (
        By.CSS_SELECTOR,
        "#orderModal > div:nth-child(1) > div:nth-child(1)",
    )
    ORDER_MODAL_CART_PRICE = (By.ID, "totalm")
    ORDER_MODAL_NAME = (By.ID, "name")
    ORDER_MODAL_COUNTRY = (By.ID, "country")
    ORDER_MODAL_CITY = (By.ID, "city")
    ORDER_MODAL_CREDIT_CARD = (By.ID, "card")
    ORDER_MODAL_MONTH = (By.ID, "month")
    ORDER_MODAL_YEAR = (By.ID, "year")
    ORDER_MODAL_PURCHASE_BUTTON = (By.CSS_SELECTOR, '[onclick="purchaseOrder()"]')
    ORDER_MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "#orderModal > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)",
    )

    # Place Order Confirmation Prompt
    CONFIRMATION_PROMPT = (By.CLASS_NAME, "sweet-alert")
    CONFIRMATION_PROMPT_MESSAGE = (By.CSS_SELECTOR, "h2")
    CONFIRMATION_PROMPT_DATA_BLOCK = (By.CLASS_NAME, "lead")
    CONFIRMATION_PROMPT_AMOUNT = (By.CSS_SELECTOR, "lead > br:nth-child(1)")
    CONFIRMATION_PROMPT_OK_BUTTON = (By.CLASS_NAME, "confirm")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_product_table_header_text(self, header: str) -> str:
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

    def get_all_product_rows(self) -> list[WebElement]:
        product_rows = self.get_all_elements(locator=self.PRODUCT_TABLE_PRODUCT_ROW)
        return product_rows

    def get_product_row_image_link(self, product_row: WebElement) -> str:
        image_link = (
            self.get_sub_element_attribute(
                parent_element=product_row,
                locator=self.PRODUCT_TABLE_PRODUCT_PIC,
                attribute="src",
            ),
        )
        return image_link[0]

    def get_product_row_title(self, product_row: WebElement) -> str:
        product_title = self.get_sub_element_text(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_TITLE
        )
        return product_title

    def get_product_row_price(self, product_row: WebElement) -> float:
        product_price = self.get_sub_element_text(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_PRICE
        )
        return float(product_price)

    def get_product_row_delete_button(self, product_row: WebElement) -> WebElement:
        element = self.get_sub_element(
            parent_element=product_row, locator=self.PRODUCT_TABLE_PRODUCT_DELETE
        )
        return element

    def create_product_rows_cards(
        self, product_rows: list[WebElement]
    ) -> list[ProductRowCard]:
        product_rows_cards = []

        for product_row in product_rows:
            new_product_row_card = ProductRowCard(
                image_link=self.get_product_row_image_link(product_row=product_row),
                title=self.get_product_row_title(product_row=product_row),
                price=self.get_product_row_price(product_row=product_row),
                delete_button=self.get_product_row_delete_button(
                    product_row=product_row
                ),
            )

            product_rows_cards.append(new_product_row_card)

        return product_rows_cards

    def get_product_card(
        self, all_cards: list[ProductRowCard], product_name: str
    ) -> ProductRowCard:
        """
        Returns a single ProductCard object or raises a ValueError if the name
        is not found.

        Args:
            all_cards (list): A list of ProductCard objects.
            product_name (str): The name of the product to be returned.
        """
        try:
            card = next(c for c in all_cards if c.title == product_name)
            return card
        except StopIteration:
            raise ValueError(
                f"'{product_name}' product can not be found in {[c.title for c in all_cards]}."
            )

    def delete_product(self, element: WebElement) -> None:
        self.click_button(locator=element)
        self.wait_for_element_to_get_stale(element=element)
        return

    def get_cart_total_price(self) -> float:
        cart_total_price = self.get_element_text(locator=self.CART_TOTAL_VALUE)
        return float(cart_total_price)

    def click_place_order_button(self) -> None:
        self.click_button(locator=self.PLACE_ORDER_BUTTON)
        return

    def get_place_order_modal(self) -> None:
        self.click_place_order_button()
        self.get_element(locator=self.PLACE_ORDER_MODAL)
        return

    def get_modal_cart_price(self, retries: int = 10) -> float:
        # the price might not be already loaded when the element text is fetched
        # so we try a couple of times until we get it
        for _ in range(retries):
            try:
                modal_cart_price = self.get_element_text(
                    locator=self.ORDER_MODAL_CART_PRICE
                )
                # remove 'Total: ' and cast the string value to a float
                modal_cart_price_value = float(modal_cart_price[6:])
                return modal_cart_price_value
            except ValueError:
                continue

        raise ValueError(
            f"Price value could not be extracted from '{modal_cart_price}' string"
            f" and cast to a float after {retries} retries"
        )

    def fill_place_order_modal_fields(
        self,
        name: str = "Jonh Smith",
        country: str = "Romania",
        city: str = "Paris",
        credit_card: str = "0123456789",
        month: str = "12",
        year: str = "1996",
    ) -> None:
        self.set_field_value(field_locator=self.ORDER_MODAL_NAME, field_value=name)
        self.set_field_value(
            field_locator=self.ORDER_MODAL_COUNTRY, field_value=country
        )
        self.set_field_value(field_locator=self.ORDER_MODAL_CITY, field_value=city)
        self.set_field_value(
            field_locator=self.ORDER_MODAL_CREDIT_CARD, field_value=credit_card
        )
        self.set_field_value(field_locator=self.ORDER_MODAL_MONTH, field_value=month)
        self.set_field_value(field_locator=self.ORDER_MODAL_YEAR, field_value=year)

    def close_place_order_modal(self) -> None:
        self.click_button(locator=self.ORDER_MODAL_CLOSE_BUTTON)
        return

    def purchase_order(self) -> None:
        self.click_button(locator=self.ORDER_MODAL_PURCHASE_BUTTON)
        return

    def get_confirmation_prompt(self) -> WebElement:
        confirmation_prompt = self.get_element(locator=self.CONFIRMATION_PROMPT)
        return confirmation_prompt

    def get_confirmation_prompt_message(self) -> str:
        parent = self.get_confirmation_prompt()
        message = self.get_sub_element_text(
            parent_element=parent, locator=self.CONFIRMATION_PROMPT_MESSAGE
        )
        return message

    def get_confirmation_prompt_data(self) -> str:
        data_block = self.get_element_text(locator=self.CONFIRMATION_PROMPT_DATA_BLOCK)
        return data_block

    def parse_confirmation_prompt_data(
        self, confirmation_prompt_data: str
    ) -> tuple[str, int, str, str, str, str]:
        data = confirmation_prompt_data.split("\n")
        order_id_raw = data[0]
        order_id_numeric = int(data[0][4:])
        order_amount = data[1]
        card_number = data[2]
        name = data[3]
        order_date = data[4]

        return (
            order_id_raw,
            order_id_numeric,
            order_amount,
            card_number,
            name,
            order_date,
        )

    def create_confirmation_prompt_expected_date(self) -> str:
        """
        Generates a formatted date string representing the expected confirmation
        prompt date.

        The adjustment of subtracting one month from the current date is
        intentional and reflects the behavior of the site under test, which
        displays the purchase confirmation date as one month earlier than the
        actual current date.

        Returns:
            str: A string formatted as "Date: DD/MM/YYYY" with the month
            adjusted back by one.
        """
        today = datetime.today()
        if today.month == 1:
            adjusted_month = 12
            adjusted_year = today.year - 1
        else:
            adjusted_month = today.month - 1
            adjusted_year = today.year

        formatted_date = today.strftime(f"{today.day}/{adjusted_month}/{adjusted_year}")
        confirmation_prompt_expected_date_data = f"Date: {formatted_date}"
        return confirmation_prompt_expected_date_data

    def create_ConfirmationPromptData(
        self, data: tuple[str, int, str, str, str, str]
    ) -> ConfirmationPromptData:
        new_ConfirmationPromptData = ConfirmationPromptData(
            order_id_raw=data[0],
            order_id_numeric=data[1],
            order_amount=data[2],
            card_number=data[3],
            name=data[4],
            order_date=data[5],
        )

        return new_ConfirmationPromptData

    def get_confirmation_data(self) -> ConfirmationPromptData:
        confirmation_prompt_data = self.get_confirmation_prompt_data()
        parsed_data = self.parse_confirmation_prompt_data(
            confirmation_prompt_data=confirmation_prompt_data
        )
        confirmation_prompt_data_object = self.create_ConfirmationPromptData(
            data=parsed_data
        )
        return confirmation_prompt_data_object

    def click_confirmation_prompt_ok_button(self) -> None:
        self.click_button(self.CONFIRMATION_PROMPT_OK_BUTTON)
        return
