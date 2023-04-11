"""
This function is mainly to access the loaded URLs during the scrolling process and save to CSV .
"""

# regex
import re

# 透過什麼方式選取元素
from selenium.webdriver.common.by import By

# 儲存資料
import pandas as pd


def get_href(driver):
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
    # To prevent interruptions or duplicate captures while scrolling,
    # first save the links for each post
    df_href = pd.DataFrame(list(links))
    df_href.to_csv("../../docs/PostsLinks.csv", header=False, index=False)
    return links
