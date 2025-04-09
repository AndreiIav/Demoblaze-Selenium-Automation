from pages.login_page import Alert, LoginPage


def test_login_valid_credentials(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)
    test_driver.get(base_url)

    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"


def test_log_out(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)
    test_driver.get(base_url)

    login_page.login(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"

    login_page.log_out()

    assert login_page.is_element_visible(login_page.NAVIGATION_LOG_IN)


def test_login_with_missing_credentials(test_driver, base_url):
    login_page = LoginPage(test_driver)
    login_alert = Alert(test_driver)
    test_driver.get(base_url)

    login_page.get_log_in_modal()
    login_page.click_log_in()

    alert_text = login_alert.get_alert_text()

    assert "Please fill out Username and Password." in alert_text


def test_login_with_wrong_password(test_driver, base_url, user_credentials):
    login_page = LoginPage(test_driver)
    login_alert = Alert(test_driver)
    test_driver.get(base_url)

    login_page.get_log_in_modal()
    login_page.set_username(user_credentials.username)
    login_page.set_password("fake password")
    login_page.click_log_in()

    alert_text = login_alert.get_alert_text()

    assert "Wrong password" in alert_text
