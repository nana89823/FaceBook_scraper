"""
This module is used to scrape information from Facebook.
Including posts, comments, likes, etc.
However, it is limited to scraping only the "Costco Taiwan 商品經驗老實說" page.

"""
# 解析命令行參數
import argparse

# 強制等待
from time import sleep

# 計算時間
from datetime import datetime

# regex
import re

# 操作 browser 的 API
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 處理逾時的例外工具
from selenium.common.exceptions import NoSuchElementException

# 透過什麼方式選取元素
from selenium.webdriver.common.by import By

# autochains
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# 儲存資料
import pandas as pd
from bs4 import BeautifulSoup as bs
import pytest


@pytest.fixture
def page():
    return "https://www.facebook.com/groups/1260448967306807"


@pytest.fixture
def num_of_post():
    return 4


@pytest.fixture
def infinite_scroll():
    return False


@pytest.fixture
def scrape_comment():
    return True


@pytest.fixture(scope="module")
def driver():
    option = Options()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=option
    )
    yield driver
    driver.quit()


@pytest.fixture
def soup():
    driver.get(link)
    soup = bs(driver.page_source, "lxml")
    return soup


@pytest.fixture
def email():
    return "your email"


@pytest.fixture
def password():
    return "your password"


@pytest.fixture
def link():
    return "https://www.facebook.com/groups/1260448967306807/posts/6659802280704755"


@pytest.fixture
def len_of_page():
    return 1


def test_login(driver, email, password):
    """
    This function is for logging into your Facebook account.

    Args:
        driver (webdriver): driver for the webpage.

        email (str): Your Email.

        password (str):Your Password.
    """

    driver.get("http://facebook.com")
    driver.maximize_window()
    driver.find_element(
        By.CSS_SELECTOR, "input.inputtext._55r1._6luy").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input.inputtext._55r1._6luy._9npi").send_keys(
        password
    )
    driver.find_element(
        By.CSS_SELECTOR, "button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy"
    ).click()
    sleep(3)


def test_count_needed_scrolls(driver, infinite_scroll, num_of_post):
    """
    This function is to calculate the total number of pages to scroll.
    And print to console.

    Args:
        driver (webdriver): driver for the webpage.

        infinite_scroll (bool): Scroll until the end of the fanPage.

        num_of_post (int): Post you want. Assume 3 post per scroll

        expected (int): The expected result of the calculation.

    return:
        None
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
    assert len_of_page == int(num_of_post / 4)
    return len_of_page


def test_scroll(driver, infinite_scroll, len_of_page):
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


def test_get_more_reply(driver):
    """
    This function is mainly to expand more replies.
    Such as "View more comments, View x replies, x replies, View previous replies.

    Args:
        driver (webdriver): driver for the webpage.
    """

    flag = True
    while flag:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
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


def test_get_href(driver):
    """
    This function is mainly to access the loaded URLs during the scrolling process and save to CSV .
    In order to avoid interruptions or retrieving duplicates.

    Args:
        driver (webdriver): driver for the webpage.
    """
    hrefs = driver.find_elements(
        By.CSS_SELECTOR,
        (
            "a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y."
            "xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r."
            "x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69."
            "xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq."
            "x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm"
        ),
    )
    links = set()
    for href in hrefs:
        href = re.search(r".+(?=\/\?)", href.get_attribute("href"))
        if href is not None:
            links.add(href[0])
    return links


def test_post_info(link, driver):
    """
    This function is mainly to access the basic information of post and save to csv.
    But excluding any type of comments.

    Args:
        driver (webdriver): driver for the webpage.

        link (str): post link ,such as "https://www.facebook.com/groups/[groupID]/posts/[postID]/"
    """

    # Get date
    place_acquisition_date = datetime.now().strftime("%Y-%m-%d")

    href = link

    name = driver.find_element(
        By.XPATH,
        """/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]
        /div[1]/div/div[2]/div/div/div[4]
        /div/div/div/div/div/div/div/div[1]
        /div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[2]
        /div/div[1]/span/span/a/div/object/a""",
    ).get_attribute("aria-label")

    try:
        post = driver.find_element(
            By.XPATH,
            """/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]
            /div[1]/div/div[2]/div/div/div[4]
            /div/div/div/div/div/div/div/div[1]
            /div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[3]
            /div[1]/div/div/div/span""",
        ).text
    except NoSuchElementException:
        post = driver.find_element(
            By.XPATH,
            """/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]
            /div[1]/div/div[2]/div/div/div[4]
            /div/div/div/div/div/div/div/div/div/div/div/div/div/
            div/div/div/div/div/div[8]/div/div/div[3]
            /div[1]/div/span/div[2]/span""",
        ).text

    try:
        likes = driver.find_element(
            By.XPATH,
            """/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]
            /div[1]/div/div[2]/div/div/div[4]
            /div/div/div/div/div/div/div/div[1]
            /div/div/div/div/div/div/div/div/div/div/div[8]
            /div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]
            /div/span/div/span[2]/span/span""",
        ).text
    except NoSuchElementException:
        likes = "0"

    try:
        comment_count = driver.find_element(
            By.XPATH,
            """/html/body/div[1]/div/div[1]/div/div[3]
            /div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]
            /div/div/div/div/div/div/div/div[1]
            /div/div/div/div/div/div/div/div/div/div/div[8]
            /div/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]
            /div[2]/span/div""",
        ).text
    except NoSuchElementException:
        comment_count = "0"

    try:
        share = driver.find_element(
            By.XPATH,
            """/html/body/div[1]/div/div[1]/div/div[3]
            /div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]
            /div/div/div/div/div/div/div/div[1]
            /div/div/div/div/div/div/div/div/div/div/div[8]
            /div/div/div[4]/div/div/div[1]/div/div[1]
                /div/div[2]/div[3]/span/div""",
        ).text
    except NoSuchElementException:
        share = "0"

    df_post_info = pd.DataFrame(
        {
            "place_acquisition_date": place_acquisition_date,
            "name": name,
            "post": post,
            "likes": [likes],
            "comment_count": [comment_count],
            "share": [share],
            "link": href,
        },
        columns=[
            "place_acquisition_date",
            "name",
            "post",
            "likes",
            "comment_count",
            "share",
            "link",
        ],
    )
    df_post_info.to_csv(
        "../docs/PostsInformation.csv", mode="a", header=False, index=False
    )


def test_post_comment(soup):
    """
    This function is mainly to access all types of replies and save to csv.
    Whether they are replies to post or comments on comments.

    Args:
        soup (BeautifulSoup): Used to parse HTML documents.
    """

    user_comment = soup.find_all(
        "div", class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi"
    )
    for i in user_comment:
        # Get date
        place_acquisition_date = datetime.now().strftime("%Y-%m-%d")
        try:
            comment = i.find(
                "div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r"
            ).get_text()
        except AttributeError:
            comment = "sticker"
        name = i.find("span", class_="x3nfvp2").get_text()
        link = i.find(
            "a",
            class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y "
            "xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r "
            "x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 "
            "xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv "
            "xi81zsa xo1l8bm",
        )["href"]
        time = i.find(
            "a",
            class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou "
            "x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm "
            "xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd "
            "x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xi81zsa xo1l8bm",
        ).get_text()
        comment_id = re.findall(r"\d+(?=\/\?|\&)", link)
        if len(comment_id) == 3:
            post_id = comment_id[0]
            comment_id = comment_id[1]
            replay_comment_id = comment_id[2]
        else:
            post_id = comment_id[0]
            comment_id = comment_id[1]
            replay_comment_id = "0"

        df_post_comment = pd.DataFrame(
            {
                "post_id": post_id,
                "place_acquisition_date": place_acquisition_date,
                "name": name,
                "time": [time],
                "comment_id": [comment_id],
                "replay_comment_id": [replay_comment_id],
                "comment": comment,
                "link": link,
            },
            columns=[
                "post_id",
                "place_acquisition_date",
                "name",
                "time",
                "comment_id",
                "replay_comment_id",
                "comment",
                "link",
            ],
        )
        df_post_comment.to_csv(
            "../docs/PostsComment.csv", mode="a", header=False, index=False
        )


def test_extract(page, num_of_post, infinite_scroll, scrape_comment):
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

    len_of_page = test_count_needed_scrolls(
        driver, infinite_scroll, num_of_post)

    test_scroll(driver, infinite_scroll, len_of_page)

    links = test_get_href(driver)

    with open("../docs/facebook_credential.txt", encoding="utf-8") as file:
        email = file.readline().split('"')[1]
        password = file.readline().split('"')[1]

    test_login(driver, email, password)

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
    posts_information.to_csv("../docs/PostsInformation.csv", index=False)

    for link in links:
        driver.get(link)

        sleep(3)

        test_post_info(link, driver)

        if scrape_comment:
            # Save DataFrame header first
            posts_comment = pd.DataFrame(
                columns=[
                    "place_acquisition_date",
                    "name",
                    "time",
                    "comment_id",
                    "replay_comment_id",
                    "comment",
                    "link",
                ]
            )
            posts_comment.to_csv("../docs/PostsComment.csv", index=False)

            test_get_more_reply(driver)

            soup = bs(driver.page_source, "lxml")

            test_post_comment(soup)
    driver.quit()
