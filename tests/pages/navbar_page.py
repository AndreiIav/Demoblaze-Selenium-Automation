from pages.base_page import BasePage
from selenium.webdriver.common.by import By


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

    def __init__(self, driver):
        super().__init__(driver)

    def get_log_in_button(self):
        log_in_button = self.get_element(self.LOG_IN_BUTTON)
        return log_in_button
