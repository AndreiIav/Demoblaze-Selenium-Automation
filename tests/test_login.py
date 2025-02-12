from pages.login_page import LoginPage


def test_login_valid_credentials(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)

    test_driver.get(base_url)
    login_page.get_log_in_modal()
    login_page.log_in(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"


def test_log_out(test_driver, user_credentials, base_url):
    login_page = LoginPage(test_driver)

    test_driver.get(base_url)
    login_page.get_log_in_modal()
    login_page.log_in(
        username=user_credentials.username, password=user_credentials.password
    )
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {user_credentials.username}"

    login_page.log_out()

    assert login_page.is_element_visible(login_page.NAVIGATION_LOG_IN)
