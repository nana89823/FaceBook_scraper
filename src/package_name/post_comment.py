"""
This function is mainly to access all types of replies and save to csv.
"""
# 計算時間
from datetime import datetime

# regex
import re

# 儲存資料
import pandas as pd


def post_comment(soup):
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
            "../../docs/PostsComment.csv", mode="a", header=False, index=False
        )
