from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LoginPage(BasePage):
    LOG_IN_MODAL = (By.ID, "logInModalLabel")
    USERNAME = (By.ID, "loginusername")
    PASSWORD = (By.ID, "loginpassword")
    MODAL_LOG_IN_BUTTON = (By.CSS_SELECTOR, '[onclick="logIn()"]')
    LOGGED_IN_USER = (By.ID, "nameofuser")
    LOG_OUT = (By.CSS_SELECTOR, '[onclick="logOut()"]')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_log_in_modal(self) -> None:
        self.get_element(self.LOG_IN_MODAL)
        return

    def clear_login_fields(self) -> None:
        self.clear_field(field_locator=self.PASSWORD)
        self.clear_field(field_locator=self.USERNAME)

    def click_log_in(self) -> None:
        log_in_button = self.get_element(self.MODAL_LOG_IN_BUTTON)
        log_in_button.click()

    def get_logged_in_user_text(self) -> str:
        self.get_element(locator=self.LOGGED_IN_USER)
        logged_in_user = self.get_element_text(locator=self.LOGGED_IN_USER)

        return logged_in_user

    def login(self, username: str, password: str) -> None:
        self.set_field_value(field_locator=self.USERNAME, field_value=username)
        self.set_field_value(field_locator=self.PASSWORD, field_value=password)
        self.click_log_in()

    def log_out(self) -> None:
        log_out_button = self.get_element(self.LOG_OUT)
        log_out_button.click()
