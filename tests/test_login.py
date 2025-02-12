from pages.login_page import LoginPage


def test_login_valid_credentials(firefox_browser):
    url = "https://www.demoblaze.com/index.html"
    username = "abc_12"
    password = "abc"

    login_page = LoginPage(firefox_browser)

    firefox_browser.get(url)
    login_page.get_log_in_modal()
    login_page.log_in(username=username, password=password)
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {username}"


def test_log_out(firefox_browser):
    url = "https://www.demoblaze.com/index.html"
    username = "abc_12"
    password = "abc"

    login_page = LoginPage(firefox_browser)

    firefox_browser.get(url)
    login_page.get_log_in_modal()
    login_page.log_in(username=username, password=password)
    logged_in_user = login_page.get_logged_in_user()

    assert logged_in_user.text == f"Welcome {username}"

    login_page.log_out()

    assert login_page.is_element_visible(login_page.NAVIGATION_LOG_IN)
