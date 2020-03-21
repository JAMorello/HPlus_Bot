import Setup
import requests
import json
import time

query_list = ["transhumanism", "cyborg", "posthumanism", "futurism", "techno-utopias", "artificial%20intelligence",
              "genetic%20manipulation", "nanotechnology"]

with open("Links_NYT.txt", "w") as file:

    for query in query_list:
        string = query.upper() + "\n"
        file.write(string)

        try:
            for i in range(100):
                page = "page=" + str(i)
                api_key = "api-key=" + Setup.NYT_API_KEY
                query_search = "q=" + query
                concatenate = "&".join([query_search, page, api_key])

                real_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?" + concatenate
                print(real_url)
                response = requests.get(real_url)
                data = json.loads(response.text)

                try:
                    for j in range(10):
                        print(query, i, j)
                        info = data["response"]["docs"][j]

                        abstract = info["abstract"].lower().replace('.', '').replace(',', '').replace(':', '').split()
                        lead_paragraph = info["lead_paragraph"].lower().replace('.', '').replace(',', '').replace(':', '').split()
                        main_headline = info["headline"]["main"].lower().replace('.', '').replace(',', '').replace(':', '').split()
                        keywords = info["keywords"]
                        if any(elem in Setup.KEYWORDS for elem in abstract) or \
                                any(elem in Setup.KEYWORDS for elem in lead_paragraph) or \
                                any(elem in Setup.KEYWORDS for elem in main_headline) or \
                                any(elem in Setup.KEYWORDS for elem in keywords):

                            url_string = info["web_url"] + "\n"
                            file.write(url_string)
                except:
                    print("Error", i, j)
                    time.sleep(10)
                    break
            time.sleep(10)  # sleep 10 seconds between calls to avoid hitting the per minute rate limit
        except:
            continue