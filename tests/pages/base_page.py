from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
        )

    def get_element(self, locator: tuple[str, str]) -> WebElement:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element

    def get_clickabale_element(
        self, locator: tuple[str, str] | WebElement
    ) -> WebElement:
        clickable_element = self.wait.until(EC.element_to_be_clickable(locator))
        return clickable_element

    def get_element_text(self, locator: tuple[str, str]) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element_text = element.text
        return element_text

    def get_sub_element_attribute(
        self, parent_element: WebElement, locator: tuple[str, str], attribute: str
    ) -> str | None:
        sub_element = self.wait.until(lambda d: parent_element.find_element(*locator))
        sub_element_attribute = sub_element.get_attribute(name=attribute)
        return sub_element_attribute

    def get_sub_element_text(
        self,
        parent_element: WebElement,
        locator: tuple[str, str],
    ) -> str:
        sub_element = self.wait.until(lambda d: parent_element.find_element(*locator))
        sub_element_text = sub_element.text
        return sub_element_text

    def get_sub_element(
        self, parent_element: WebElement, locator: tuple[str, str]
    ) -> WebElement:
        sub_element = self.wait.until(lambda d: parent_element.find_element(*locator))
        return sub_element

    def get_all_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        all_elements = self.wait.until(EC.presence_of_all_elements_located(locator))
        return all_elements

    def check_if_text_is_present_in_element(
        self, locator: tuple[str, str], text: str
    ) -> None:
        self.wait.until(EC.text_to_be_present_in_element((locator), text))

    def wait_for_element_to_get_stale(self, element: WebElement) -> None:
        self.wait.until(EC.staleness_of(element))
        return

    def get_alert(self) -> Alert:
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert

    def get_alert_text(self) -> str:
        alert = self.get_alert()
        alert_text = alert.text
        return alert_text

    def accept_alert(self) -> None:
        alert = self.get_alert()
        alert.accept()
