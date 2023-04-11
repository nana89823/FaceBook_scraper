"""
This function is mainly used to implement scrolling on a webpage.
"""
# 強制等待
from time import sleep


def scroll(driver, infinite_scroll, len_of_page):
    """
    This function is mainly used to implement scrolling on a webpage.

    Args:
        driver (webdriver): driver for the webpage.

        infinite_scroll (bool): Scroll until the end of the fanPage.

        len_of_page (int) : At least how many times need to be scrolled
    """

    # Scroll the scroll bar to load the tags in the browser
    last_count = -1
    match = False

    while not match:
        if infinite_scroll:
            last_count = len_of_page
        else:
            last_count += 1

        sleep(5)

        if infinite_scroll:
            len_of_page = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
                "var len_of_page=document.body.scrollHeight;"
                "return len_of_page;"
            )
        else:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
                "var len_of_page=document.body.scrollHeight;"
                "return len_of_page;"
            )

        if last_count == len_of_page:
            match = True
