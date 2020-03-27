import requests
from bs4 import BeautifulSoup


def random_page():
    """
    This functions goes to the Random Articles section of the Main Page of H+Pedia wiki.
    Scraps the link and title of the first article an that section. Returns link and title
    in a formatted sentence to be posted in Twitter.
    """
    response = requests.get("https://hpluspedia.org/wiki/Main_Page")
    soup_parsed_response = BeautifulSoup(response.text, 'html.parser')

    first_random_page = soup_parsed_response.select('.randomPages')[0].find('li')
    url = 'https://hpluspedia.org' + first_random_page.a['href']
    title = first_random_page.a['title']
    return f"Learn more about {title} in HPlusPedia! Go to: {url}"
