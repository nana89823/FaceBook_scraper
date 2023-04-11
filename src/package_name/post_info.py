"""
This function is mainly to access the basic information of post and save to csv.
"""
# 計算時間
from datetime import datetime

# 處理逾時的例外工具
from selenium.common.exceptions import NoSuchElementException

# 透過什麼方式選取元素
from selenium.webdriver.common.by import By

# 儲存資料
import pandas as pd


def post_info(link, driver):
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
        "../../docs/PostsInformation.csv", mode="a", header=False, index=False
    )
