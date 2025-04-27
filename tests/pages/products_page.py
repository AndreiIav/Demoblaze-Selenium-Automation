from dataclasses import dataclass

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


@dataclass
class ProductCard:
    image_link: str
    title: str
    title_link: str
    price: float
    description: str


class ProductsPage(BasePage):
    # Categories
    PHONES = (By.CSS_SELECTOR, "[onclick=\"byCat('phone')\"]")
    LAPTOPS = (By.CSS_SELECTOR, "[onclick=\"byCat('notebook')\"]")
    MONITORS = (By.CSS_SELECTOR, "[onclick=\"byCat('monitor')\"]")

    # Cards
    CARD = (By.CLASS_NAME, "card")
    CARD_IMAGE_LINK = (By.CSS_SELECTOR, ".card > a")
    CARD_PRODUCT_TITLE = (By.CLASS_NAME, "hrefch")
    CARD_PRODUCT_PRICE = (By.CSS_SELECTOR, ".card-block > h5")
    CARD_PRODUCT_DESCRIPTION = (By.CLASS_NAME, "card-text")

    def __init__(self, driver):
        super().__init__(driver)

    def click_categories_button(self, category_button):
        if category_button == "phones":
            category_selector = self.PHONES
        elif category_button == "laptops":
            category_selector = self.LAPTOPS
        elif category_button == "monitors":
            category_selector = self.MONITORS
        else:
            raise ValueError(f"'{category_button}' is not a valid categories button.")

        self.is_element_visible(category_selector)
        phones_button = self.driver.find_element(*category_selector)
        phones_button.click()

    def get_all_cards_on_page(self):
        self.is_element_visible(self.CARD)
        all_cards = self.driver.find_elements(*self.CARD)
        return all_cards

    def get_all_cards_links(self, link_origin):
        if link_origin == "card_image":
            link_selector = self.CARD_IMAGE_LINK
        elif link_origin == "card_title":
            link_selector = self.CARD_PRODUCT_TITLE
        else:
            raise ValueError(f"'{link_origin}' is not a valid link selector.")

        self.is_element_visible(link_selector)
        all_image_links = self.driver.find_elements(*link_selector)
        all_cards_image_links = [
            image_link.get_attribute("href") for image_link in all_image_links
        ]
        return all_cards_image_links

    def get_all_cards_titles(self):
        self.is_element_visible(self.CARD_PRODUCT_TITLE)
        all_cards = self.driver.find_elements(*self.CARD_PRODUCT_TITLE)
        all_card_titles = [card.text for card in all_cards]
        return all_card_titles

    def get_all_cards_prices(self):
        self.is_element_visible(self.CARD_PRODUCT_PRICE)
        all_prices_elements = self.driver.find_elements(*self.CARD_PRODUCT_PRICE)
        all_card_prices = [float(card.text[1:]) for card in all_prices_elements]
        return all_card_prices

    def get_all_cards_descriptions(self):
        self.is_element_visible(self.CARD_PRODUCT_DESCRIPTION)
        all_description_elements = self.driver.find_elements(
            *self.CARD_PRODUCT_DESCRIPTION
        )
        all_cards_descriptions = [card.text for card in all_description_elements]
        return all_cards_descriptions

    def create_products_cards(
        self,
        all_cards,
        all_image_links,
        all_title_links,
        all_card_titles,
        all_card_prices,
        all_card_descriptions,
    ):
        product_cards = []

        for i in range(len(all_cards)):
            card = ProductCard(
                image_link=all_image_links[i],
                title=all_card_titles[i],
                title_link=all_title_links[i],
                price=all_card_prices[i],
                description=all_card_descriptions[i],
            )
            product_cards.append(card)

        product_cards.sort(key=lambda x: "title")

        return product_cards

    def get_product_cards(self):
        product_cards = self.create_products_cards(
            all_cards=self.get_all_cards_on_page(),
            all_image_links=self.get_all_cards_links(link_origin="card_image"),
            all_title_links=self.get_all_cards_links(link_origin="card_title"),
            all_card_titles=self.get_all_cards_titles(),
            all_card_prices=self.get_all_cards_prices(),
            all_card_descriptions=self.get_all_cards_descriptions(),
        )

        return product_cards
