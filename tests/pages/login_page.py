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

    def get_log_in_modal(self, log_in_button):
        log_in_button.click()
        if self.check_if_element_is_visible(self.LOG_IN_MODAL):
            return True
        else:
            raise LookupError("Log_in modal not present")

    def set_username(self, username):
        username_box = self.get_element(locator=self.USERNAME)
        username_box.send_keys(username)

    def set_password(self, password):
        password_box = self.get_element(locator=self.PASSWORD)
        password_box.send_keys(password)

    def click_log_in(self):
        log_in_button = self.get_element(self.MODAL_LOG_IN_BUTTON)
        log_in_button.click()

    def clear_username_box(self):
        username_box = self.get_element(locator=self.USERNAME)
        username_box.clear()

    def clear_password_box(self):
        password_box = self.get_element(locator=self.PASSWORD)
        password_box.clear()

    def get_logged_in_user(self):
        self.check_if_text_is_present_in_element(
            locator=(self.LOGGED_IN_USER), text=self.WELCOME_USER_TEXT
        )
        logged_in_user = self.driver.find_element(*self.LOGGED_IN_USER)

        return logged_in_user

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_log_in()

    def log_out(self):
        log_out_button = self.get_element(self.LOG_OUT)
        log_out_button.click()
