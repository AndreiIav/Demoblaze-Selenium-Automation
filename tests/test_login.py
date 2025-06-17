from pages.login_page import LoginPage
from pages.navbar_page import NavbarPage


def test_login_valid_credentials(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)
    expected_logged_in_user_text = f"Welcome {user_credentials.username}"

    navbar_page.click_button(button="log in")
    login_page.get_log_in_modal()
    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user_text = login_page.get_logged_in_user_text()

    assert logged_in_user_text == expected_logged_in_user_text


def test_login_with_missing_credentials(test_driver, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)
    expected_alert_text = "Please fill out Username and Password."

    navbar_page.click_button(button="log in")
    login_page.get_log_in_modal()
    login_page.click_log_in()
    alert_text = login_page.get_alert_text()

    assert expected_alert_text in alert_text


def test_login_with_wrong_password(test_driver, base_url, user_credentials):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)
    test_wrong_password = "fake password"
    expected_alert_text = "Wrong password"

    navbar_page.click_button(button="log in")
    login_page.get_log_in_modal()
    login_page.login(username=user_credentials.username, password=test_wrong_password)
    alert_text = login_page.get_alert_text()

    assert expected_alert_text in alert_text


def test_login_with_inexistent_user(test_driver, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)
    test_inexistent_user = "lsfjdsjdfosidufksmdfls!!!!"
    test_wrong_password = "fake password"
    expected_alert_text = "User does not exist"

    navbar_page.click_button(button="log in")
    login_page.get_log_in_modal()
    login_page.login(username=test_inexistent_user, password=test_wrong_password)
    alert_text = login_page.get_alert_text()

    assert expected_alert_text in alert_text


def test_successful_login_after_initial_failed_attempt(
    test_driver, base_url, user_credentials
):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)
    expected_logged_in_user_text = f"Welcome {user_credentials.username}"
    test_inexistent_user = "lsfjdsjdfosidufksmdfls!!!!"
    test_wrong_password = "fake password"

    navbar_page.click_button(button="log in")
    login_page.get_log_in_modal()
    login_page.login(username=test_inexistent_user, password=test_wrong_password)
    login_page.accept_alert()
    login_page.clear_login_fields()
    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user_text = login_page.get_logged_in_user_text()

    assert logged_in_user_text == expected_logged_in_user_text
