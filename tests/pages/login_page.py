from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    LOG_IN_MODAL = (By.ID, "logInModalLabel")
    USERNAME = (By.ID, "loginusername")
    PASSWORD = (By.ID, "loginpassword")
    MODAL_LOG_IN_BUTTON = (By.CSS_SELECTOR, '[onclick="logIn()"]')
    LOGGED_IN_USER = (By.ID, "nameofuser")
    LOG_OUT = (By.CSS_SELECTOR, '[onclick="logOut()"]')
    WELCOME_USER_TEXT = "Welcome"

    def __init__(self, driver):
        super().__init__(driver)

    def get_log_in_modal(self):
        self.check_if_element_is_visible(self.LOG_IN_MODAL)
        return

    def fill_field(self, field_locator, field_value):
        field = self.get_element(locator=field_locator)
        field.send_keys(field_value)

    def clear_field(self, field_locator):
        field = self.get_element(locator=field_locator)
        field.clear()

    def clear_login_fields(self):
        self.clear_field(field_locator=self.PASSWORD)
        self.clear_field(field_locator=self.USERNAME)

    def click_log_in(self):
        log_in_button = self.get_element(self.MODAL_LOG_IN_BUTTON)
        log_in_button.click()

    def get_logged_in_user_text(self):
        self.check_if_text_is_present_in_element(
            locator=self.LOGGED_IN_USER, text=self.WELCOME_USER_TEXT
        )
        logged_in_user = self.get_element_text(locator=self.LOGGED_IN_USER)

        return logged_in_user

    def login(self, username, password):
        self.fill_field(field_locator=self.USERNAME, field_value=username)
        self.fill_field(field_locator=self.PASSWORD, field_value=password)
        self.click_log_in()

    def log_out(self):
        log_out_button = self.get_element(self.LOG_OUT)
        log_out_button.click()
