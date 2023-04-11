"""
This module is used to scrape information from Facebook.
Including posts, comments, likes, etc.
However, it is limited to scraping only the "Costco Taiwan 商品經驗老實說" page.

"""
# 解析命令行參數
import argparse
from extract import extract

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook Page Scraper")
    required_parser = parser.add_argument_group("required arguments")
    required_parser.add_argument(
        "-page", "-p", help="The Facebook Public Page you want to scrape", required=True
    )
    required_parser.add_argument(
        "-len",
        "-l",
        help="""Number of Posts you want to scrape,
                              The default is at least 4 posts,
                              input less than 4 is equal to the default.
                            """,
        type=int,
        required=True,
    )
    optional_parser = parser.add_argument_group("optional arguments")
    optional_parser.add_argument(
        "-INFINITE",
        "-i",
        help="Scroll until the end of the page (1 = INFINITE) (Default is 0)",
        type=int,
        default=0,
    )

    optional_parser.add_argument(
        "-comments",
        "-c",
        help="Scrape ALL Comments of Posts (y/n) (Default is n). When "
        "enabled for pages where there are a lot of comments it can "
        "take a while",
        default="No",
    )
    args = parser.parse_args()

    INFINITE = False
    if args.INFINITE == 1:
        INFINITE = True

    SCRAPE_COMMENT = False
    if args.comments == "y":
        SCRAPE_COMMENT = True

    extract(
        page=args.page,
        num_of_post=args.len,
        infinite_scroll=INFINITE,
        scrape_comment=SCRAPE_COMMENT,
    )

    print("Finished")
