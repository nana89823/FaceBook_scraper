"""
This function is mainly to expand more replies.
"""
# 強制等待
from time import sleep

# regex
import re

# autochains
from selenium.webdriver.common.action_chains import ActionChains

# 透過什麼方式選取元素
from selenium.webdriver.common.by import By


def get_more_reply(driver):
    """
    This function is mainly to expand more replies.
    Such as "View more comments, View x replies, x replies, View previous replies.

    Args:
        driver (webdriver): driver for the webpage.
    """

    flag = True
    while flag:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        # Find elements such as "View more comments
        # View x replies, x replies, View previous replies
        more_reply = driver.find_elements(
            By.CSS_SELECTOR, "span.x78zum5.x1w0mnb.xeuugli"
        )
        if more_reply != []:
            # To avoid clicking on hidden messages.
            count = 0
            for i in more_reply:
                hidden_comment = re.search("隱藏", i.text)
                if hidden_comment is None:
                    action = ActionChains(driver)
                    action.move_to_element(i).click(i).perform()
                    sleep(1)
                else:
                    count += 1
                    if count == len(more_reply):
                        flag = False
                        break
        else:
            break
