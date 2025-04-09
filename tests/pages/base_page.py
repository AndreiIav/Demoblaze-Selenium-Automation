from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver=self.driver, timeout=10)

    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_all_elements_located(locator=locator))
            return True
        except Exception:
            return False

    def is_text_present_in_element(self, locator, text):
        try:
            self.wait.until(EC.text_to_be_present_in_element((locator), text))
            return True
        except Exception:
            return False

    def get_alert(self):
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert
        except Exception:
            print("no alert showed up")
