"""
This function is to calculate the total number of pages to scroll.
    And print to console.
"""


def count_needed_scrolls(driver, infinite_scroll, num_of_post):
    """
    This function is to calculate the total number of pages to scroll.
    And print to console.

    Args:
        driver (webdriver): driver for the webpage.

        infinite_scroll (bool): Scroll until the end of the fanPage.

        num_of_post (int): Post you want. Assume 3 post per scroll

    return:
        int: height to scroll.
    """

    # To calculate how many times the input needs to be scrolled.
    if infinite_scroll:
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
            "var len_of_page=document.body.scrollHeight;"
            "return len_of_page;"
        )
    else:
        # 4 post per scroll
        len_of_page = int(num_of_post / 4)
    print("Number of times to scroll" + str(len_of_page))
    return len_of_page
