import Setup
from twitterbot_utilities import word_list, trim_title, load_links_to_post, store_links_to_post
import json
import time
import random
import requests
# https://requests.readthedocs.io/en/master/
from bs4 import BeautifulSoup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

API_LINK = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
# Check https://developer.nytimes.com/

QUERY_LIST = ["transhumanism", "cyborg", "posthumanism", "futurism", "techno-utopias", "artificial intelligence",
              "genetic manipulation", "nanotechnology"]

LINKS_NYT_FILE = "Links_NYT.txt"
LINKS_TO_POST_FILE = "Links_to_post.txt"


def scrapper():
    """
    Inserts in a list all the links in Links_to_post.txt. Grabs a random link, scraps the title of the article and the
    date of publication. Returns the title, date, and link, in a formatted sentence to be posted in Twitter. After that,
    it deletes the link (deletes the item in the list of links) and overwrites the .txt file with the remaining links.
    This is needed to make sure no link is repeated and posted again; every link must be posted only once.
    """
    links_list = load_links_to_post(LINKS_TO_POST_FILE)
    index = int(random.random() * len(links_list))

    response = requests.get(links_list[index])
    soup_parsed_response = BeautifulSoup(response.text, 'html.parser')
    string = soup_parsed_response.find('title').text
    trimmed_title = trim_title(string)
    if len(trimmed_title) > 100:
        title = trimmed_title[:100]+'...'
    else:
        title = trimmed_title
    date = soup_parsed_response.find("meta", attrs={"name": "pdate"})["content"][0:4]
    print("Tweeting article from NYT")

    store_links_to_post(links_list, index, LINKS_TO_POST_FILE)

    return f"Read a New York Times article from {date} titled \"{title}\". Go to: {links_list[index]}"


def gather_data():
    """
    This function calls the New York Times API with a list of query to gather links of articles that comply with the
    keywords criteria and saves them in a file.
    An url is used to call the API. That url contains a json file with 10 articles and the API can be accessed through
    100 pages; so a maximum of 1000 articles can be searched. Not all query searches have 1000 articles. As the API has
    a limit rate of 10 requests per minute, the function should sleep 6 second every 10 pages looked at. But while using
    the function, is found that the sleep should be of 1 minute every page. So, a sleep of 6 seconds is used by article
    looked at.
    This function returned 866 links the first time called.
    DISCLAIMER: I had a lot of trouble with the query (standard Lucene syntax), i.e. the filters query fields. So I
    left aside filters like date and sections. This has as consequence the return of a lot on trash-data I had to
    manually check and delete.
    """
    num_links = 0
    with open(LINKS_NYT_FILE, "w") as file:

        for query in QUERY_LIST:
            subject = query.upper() + "\n"
            file.write(subject)

            try:
                for i in range(100):
                    payload = {
                        "q": query,
                        "page": str(i),
                        "api-key": Setup.NYT_API_KEY
                    }
                    response = requests.get(API_LINK, params=payload)
                    print(response.url)
                    data = json.loads(response.text)

                    try:
                        for j in range(10):
                            print(query, i, j)
                            info = data["response"]["docs"][j]

                            abstract = word_list(info["abstract"])
                            lead_paragraph = word_list(info["lead_paragraph"])
                            main_headline = word_list(info["headline"]["main"])
                            keywords = info["keywords"]

                            if any(elem in Setup.KEYWORDS for elem in abstract) or \
                                    any(elem in Setup.KEYWORDS for elem in lead_paragraph) or \
                                    any(elem in Setup.KEYWORDS for elem in main_headline) or \
                                    any(elem in Setup.KEYWORDS for elem in keywords):

                                num_links += 1
                                print(num_links)
                                url_string = info["web_url"] + "\n"
                                file.write(url_string)

                            time.sleep(6)
                    except Exception:  # raises error as there are no more articles in the page
                        break
                    time.sleep(10)  # sleep 10 seconds between calls to avoid hitting the per minute rate limit
            except Exception:  # raises error as there are no more pages of the query
                continue  # goes to the next query search
