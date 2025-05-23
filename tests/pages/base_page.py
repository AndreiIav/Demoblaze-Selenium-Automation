from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
        )

    def get_element(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element

    def get_clickabale_element(self, locator):
        clickable_element = self.wait.until(EC.element_to_be_clickable(locator))
        return clickable_element

    def get_element_text(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element_text = element.text
        return element_text

    def get_sub_element_attribute(self, parent_element, locator, attribute):
        sub_element = self.wait.until(lambda d: parent_element.find_element(*locator))
        sub_element_attribute = sub_element.get_attribute(attribute)
        return sub_element_attribute

    def get_sub_element_text(
        self,
        parent_element,
        locator,
    ):
        sub_element = self.wait.until(lambda d: parent_element.find_element(*locator))
        sub_element_text = sub_element.text
        return sub_element_text

    def get_all_elements(self, locator):
        all_elements = self.wait.until(EC.presence_of_all_elements_located(locator))
        return all_elements

    def check_if_element_is_visible(self, locator) -> bool:
        return self.wait.until(EC.visibility_of_element_located(locator=locator))

    def check_if_text_is_present_in_element(self, locator, text):
        self.wait.until(EC.text_to_be_present_in_element((locator), text))

    def get_alert(self):
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert
        except Exception:
            print("no alert showed up")

    def get_alert_text(self):
        alert = self.get_alert()
        alert_text = alert.text
        return alert_text

    def accept_alert(self):
        alert = self.get_alert()
        alert.accept()
