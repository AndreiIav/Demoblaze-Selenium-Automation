from dataclasses import dataclass

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage


@dataclass
class ProductCard:
    """Represents a product card with all its details"""

    image_link: str
    title: str
    title_link: str
    price: float
    description: str


class ProductsPage(BasePage):
    # Categories buttons
    PHONES = (By.CSS_SELECTOR, "[onclick=\"byCat('phone')\"]")
    LAPTOPS = (By.CSS_SELECTOR, "[onclick=\"byCat('notebook')\"]")
    MONITORS = (By.CSS_SELECTOR, "[onclick=\"byCat('monitor')\"]")

    # Product cards
    CARD = (By.CLASS_NAME, "card")
    CARD_IMAGE_LINK = (By.CSS_SELECTOR, ".card > a")
    CARD_PRODUCT_TITLE = (By.CSS_SELECTOR, ".card-title > a")
    CARD_PRODUCT_PRICE = (By.CSS_SELECTOR, ".card-block > h5")
    CARD_PRODUCT_DESCRIPTION = (By.ID, "article")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def click_categories_button(self, category_button: str) -> None:
        CATEGORY_BUTTONS = {
            "phones": self.PHONES,
            "laptops": self.LAPTOPS,
            "monitors": self.MONITORS,
        }

        try:
            category_selector = CATEGORY_BUTTONS[category_button]
        except KeyError:
            raise KeyError(f"{category_button} is not a valid category button")

        phones_button = self.get_clickable_element(locator=category_selector)
        phones_button.click()

    def get_all_cards_on_page(self) -> list[WebElement]:
        all_cards = self.get_all_elements(self.CARD)
        return all_cards

    def get_card_link(self, card: WebElement, link_origin: str) -> str:
        if link_origin == "card_image":
            link_selector = self.CARD_IMAGE_LINK
        elif link_origin == "card_title":
            link_selector = self.CARD_PRODUCT_TITLE
        else:
            raise ValueError(f"'{link_origin}' is not a valid link selector.")

        card_link = self.get_sub_element_attribute(
            parent_element=card, locator=link_selector, attribute="href"
        )
        return card_link

    def get_card_title(self, card: WebElement) -> str:
        card_title = self.get_sub_element_text(
            parent_element=card,
            locator=self.CARD_PRODUCT_TITLE,
        )
        return card_title

    def get_card_price(self, card: WebElement) -> float:
        card_price = self.get_sub_element_text(
            parent_element=card, locator=self.CARD_PRODUCT_PRICE
        )
        # remove the '$' sign and cast the string value to a float
        card_price_value = float(card_price[1:])
        return card_price_value

    def get_card_description(self, card: WebElement) -> str:
        card_description = self.get_sub_element_text(
            parent_element=card, locator=self.CARD_PRODUCT_DESCRIPTION
        )
        return card_description

    def click_product_link(self, product_name: str) -> None:
        product_link = self.get_element(locator=(By.LINK_TEXT, product_name))
        product_link.click()

    def create_products_cards(self, cards: list[WebElement]) -> list[ProductCard]:
        """Creates ProductCard objects from the data passsed in cards argument"""
        product_cards = []

        for card in cards:
            new_card = ProductCard(
                title_link=self.get_card_link(card=card, link_origin="card_image"),
                image_link=self.get_card_link(card=card, link_origin="card_title"),
                title=self.get_card_title(card=card),
                price=self.get_card_price(card=card),
                description=self.get_card_description(card=card),
            )
            product_cards.append(new_card)

        return product_cards

    def get_all_product_cards(self, retries: int = 10) -> list[ProductCard]:
        """
        Returns ProductCard objects.

        This method returns a list of all ProductCard objects that can be created
        with products data from a single products page.
        """

        for _ in range(retries):
            try:
                all_cards_on_page = self.get_all_cards_on_page()
                all_cards = self.create_products_cards(cards=all_cards_on_page)
            except (StaleElementReferenceException, TimeoutException):
                continue

        return all_cards

    def get_product_card(
        self, all_cards: list[ProductCard], product_name: str
    ) -> ProductCard:
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
                f"'{product_name}' product can not be found in: {[c.title for c in all_cards]}."
            )
