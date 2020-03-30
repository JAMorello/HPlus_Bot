import requests
# https://requests.readthedocs.io/en/master/
from bs4 import BeautifulSoup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

HPLUSPEDIA_MAINPAGE = "https://hpluspedia.org/wiki/Main_Page"
HPLUSPEDIA_URL = 'https://hpluspedia.org'


def random_page():
    """
    This functions goes to the Random Articles section of the Main Page of H+Pedia wiki.
    Scraps the link and title of the first article an that section. Returns link and title
    in a formatted sentence to be posted in Twitter.
    """
    response = requests.get(HPLUSPEDIA_MAINPAGE)
    soup_parsed_response = BeautifulSoup(response.text, 'html.parser')

    first_random_page = soup_parsed_response.select('.randomPages')[0].find('li')
    url = HPLUSPEDIA_URL + first_random_page.a['href']
    title = first_random_page.a['title']
    print("Tweeting random page from H+Pedia")
    return f"Learn more about {title} in HPlusPedia! Go to: {url}"
