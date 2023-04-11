# 強制等待
from time import sleep
# 操作 browser 的 API
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# 儲存資料
import pandas as pd
from bs4 import BeautifulSoup as bs
from post_info import post_info
from scroll import scroll
from count_needed_scrolls import count_needed_scrolls
from login import login
from get_href import get_href
from post_comment import post_comment
from get_more_reply import get_more_reply


def extract(page, num_of_post, infinite_scroll, scrape_comment):
    """
    This function is the core of this program.

    Args:
        page (str): URL you want to scraper.

        num_of_post (int): numbers of post you want to scraper.

        infinite_scroll (bool): Scroll until the end of the fanPage

        scrape_comment (bool): scraper comments or not.
    """

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-popup-blocking")
    option.add_argument("--disable-notifiactions")
    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=option
    )

    driver.get(page)

    len_of_page = count_needed_scrolls(driver, infinite_scroll, num_of_post)

    scroll(driver, infinite_scroll, len_of_page)

    links = get_href(driver)

    with open("../../docs/facebook_credentials.txt", encoding="utf-8") as file:
        email = file.readline().split('"')[1]
        password = file.readline().split('"')[1]

    login(driver, email, password)

    # Save DataFrame header first
    posts_information = pd.DataFrame(
        columns=[
            "place_acquisition_date",
            "name",
            "post",
            "likes",
            "comment_count",
            "share",
            "link",
        ]
    )
    posts_information.to_csv("../../docs/PostsInformation.csv", index=False)

    for link in links:
        driver.get(link)

        sleep(3)

        post_info(link, driver)

        if scrape_comment:
            # Save DataFrame header first
            posts_comment = pd.DataFrame(
                columns=[
                    "post_id",
                    "place_acquisition_date",
                    "name",
                    "time",
                    "comment_id",
                    "replay_comment_id",
                    "comment",
                    "link",
                ]
            )
            posts_comment.to_csv("../../docs/PostsComment.csv", index=False)

            get_more_reply(driver)

            soup = bs(driver.page_source, "lxml")

            post_comment(soup)
    driver.quit()
