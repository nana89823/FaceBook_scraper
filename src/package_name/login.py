"""
This function is for logging into your Facebook account.
"""
# 強制等待
from time import sleep

# 透過什麼方式選取元素
from selenium.webdriver.common.by import By


def login(driver, email, password):
    """
    This function is for logging into your Facebook account.

    Args:
        driver (webdriver): driver for the webpage.

        email (str): Your Email.

        password (str):Your Password.
    """

    driver.get("http://facebook.com")
    driver.maximize_window()
    driver.find_element(By.CSS_SELECTOR, "input.inputtext._55r1._6luy").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input.inputtext._55r1._6luy._9npi").send_keys(
        password
    )
    driver.find_element(
        By.CSS_SELECTOR, "button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy"
    ).click()
    sleep(3)
