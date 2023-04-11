# FaceBook FanPage Scraper with selenium

without an API key But the groupID is only to 1260448967306807

Project Structure

```
│  README.md
│  requirements.txt
│
├─docs
│  └─output_example
│          PostsComment.csv
│          PostsInformation.csv
│          PostsLinks.csv
│────facebook_credential.txt
│
├─src
│  └─package_name
│          count_needed_scrolls.py
│          extract.py
│          get_href.py
│          get_more_reply.py
│          init.py
│          login.py
│          main.py
│          post_comment.py
│          post_info.py
│          scroll.py
│
├─tests
│      facebook_scraper_test.py

```
### Prerequisites

Place your Facebook login info into facebook_credential.txt
Logging in to a Facebook account is necessary 
To ensure that the program runs smoothly without interruptions such as being prompted to log in during the execution process.

### Installing

```
pip install -r requirements.txt
```
### Coding style

Follow PEP8 unless explicitly specified otherwise

## Deployment

Use main.py to scraper and save to csv
```
python main.py [-h] -page PAGE -len LEN [-infinite INFINITE] [-comments COMMENTS]

optional arguments:
  -h, --help            show this help message

required arguments:
  -page PAGE, -p PAGE   The FaceBook FanPage you want to scrape
  -len LEN, -l LEN      Number of Posts you want to scrape

optional arguments:
  -infinite INFINITE, -i INFINITE
                        Scroll until the end of the page (1 = infinite)
                        (Default is 0)
  -comments COMMENTS, -c COMMENTS
                        Scrape ALL Comments of Posts (y/n) (Default is n).
```
The crawled data will be stored in the "docs/" folder And the example output can be found in the "docs/output_example" folder.

## Versioning

python version at least 3.7 

## Authors

* **Mason Lin** - *Initial work* - [nana89823](https://github.com/nana89823)

## Acknowledgments

* Thank you to all the people who release code on GitHub.

