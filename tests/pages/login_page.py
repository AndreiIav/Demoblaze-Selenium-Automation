from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    NAVIGATION_LOG_IN = (By.ID, "login2")
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
        self.is_element_visible((By.ID, "navbarExample"))
        log_in_button = self.driver.find_element(*self.NAVIGATION_LOG_IN)
        log_in_button.click()
        self.is_element_visible(self.LOG_IN_MODAL)

    def log_in(self, username, password):
        username_box = self.driver.find_element(*self.USERNAME)
        password_box = self.driver.find_element(*self.PASSWORD)
        log_in_button = self.driver.find_element(*self.MODAL_LOG_IN_BUTTON)

        username_box.send_keys(username)
        password_box.send_keys(password)
        log_in_button.click()

    def get_logged_in_user(self):
        self.is_text_present_in_element(
            locator=(self.LOGGED_IN_USER), text=self.WELCOME_USER_TEXT
        )
        logged_in_user = self.driver.find_element(*self.LOGGED_IN_USER)

        return logged_in_user

    def log_out(self):
        log_out_button = self.driver.find_element(*self.LOG_OUT)
        log_out_button.click()
