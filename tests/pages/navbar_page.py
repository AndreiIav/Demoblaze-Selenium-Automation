from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class NavbarPage(BasePage):
    NAVBAR = (By.ID, "navbarExample")
    HOME_BUTTON = (
        By.CSS_SELECTOR,
        'li[class="nav-item active"] > a[href="index.html"]',
    )
    CONTACT_BUTTON = (By.CSS_SELECTOR, 'a[data-target="#exampleModal"]')
    ABOUT_US_BUTTON = (By.CSS_SELECTOR, 'a[data-target="#videoModal"]')
    CART_BUTTON = (By.ID, "cartur")
    LOG_IN_BUTTON = (By.ID, "login2")
    WELCOME_USER_TEXT = "Welcome"
    LOGGED_IN_USER = (By.ID, "nameofuser")
    LOG_OUT_BUTTON = (By.CSS_SELECTOR, '[onclick="logOut()"]')
    SIGN_UP_BUTTON = (By.ID, "signin2")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def click_navbar_button(self, button: str) -> None:
        BUTTONS = {
            "cart": self.CART_BUTTON,
            "home": self.HOME_BUTTON,
            "log in": self.LOG_IN_BUTTON,
        }

        try:
            locator = BUTTONS[button]
        except KeyError:
            raise KeyError(f"'{button}' is not a valid navbar button")

        self.click_button(locator=locator)
