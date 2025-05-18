from pages.login_page import LoginPage
from pages.navbar_page import NavbarPage


def test_login_valid_credentials(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"


def test_log_out(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"

    login_page.log_out()

    assert navbar_page.check_if_element_is_visible(navbar_page.LOG_IN_BUTTON)


def test_login_with_missing_credentials(test_driver, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.click_log_in()

    alert_text = login_page.get_alert_text()

    assert "Please fill out Username and Password." in alert_text


def test_login_with_wrong_password(test_driver, base_url, user_credentials):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.login(username=user_credentials.username, password="fake password")

    alert_text = login_page.get_alert_text()

    assert "Wrong password" in alert_text


def test_login_with_inexistent_user(test_driver, base_url):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.login(username="lsfjdsjdfosidufksmdfls!!!!", password="fake password")

    alert_text = login_page.get_alert_text()

    assert "User does not exist" in alert_text


def test_successful_login_after_initial_failed_attempt(
    test_driver, base_url, user_credentials
):
    login_page = LoginPage(test_driver)
    navbar_page = NavbarPage(test_driver)
    test_driver.get(base_url)

    log_in_button = navbar_page.get_log_in_button()
    login_page.get_log_in_modal(log_in_button)
    login_page.login(username="lsfjdsjdfosidufksmdfls!!!!", password="fake password")
    login_page.accept_alert()

    login_page.clear_username_box()
    login_page.clear_password_box()

    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"
