import json


def to_json(twitter_object):
    # The object that the API give us about the user or the tweets is messy.
    # We need a json to properly access the data.
    json_str = json.dumps(twitter_object._json)  # convert to string
    return json.loads(json_str)  # deserialise string into python object


def word_list(string):
    """
    Utility function. Deletes punctuation of the abstract, lead paragraph, and main headline of a
    New York Times articles. This is needed to facilitate the search of matching keywords (else,
    a lot of articles won´t pass the criteria because that punctuation)
    """
    return string.lower().replace('.', '').replace(',', '').replace(':', '').split()


def trim_title(string):
    """
    Utility function. Deletes certain strings from the title of a New York Time article.
    """
    title = string.replace(" - The New York Times", "").replace("IE=e ", "")\
                          .replace("Blog ", "").replace("NYT_ ", "").replace(" - International Herald Tribune", "")\
                          .replace("- Editorials & Commentary", "").replace("Opinion | ", "")\
                          .replace("TECHNOLOGY; ", "").replace("ART;\n", "").replace("PERFORMANCE ART;", "")\
                          .replace("ESSAY; ", "").replace("ALT / ", "").replace("Review/Film;   ", "")\
                          .replace("NOTICED; ", "").replace("DOWNTIME; ", "").replace("PERFORMANCE ART;", "")\
                          .replace("Technology: CONNECTIONS;", "").replace("PERFORMANCE \n", "")
    return title


def reduce_data(old_file, new_file):
    """
    Utility function. Takes the links in a file, deletes all duplicates, and creates a new file with the remaining links
    """
    links_list = list()

    with open(old_file, "r") as file:
        for line in file:
            link = line.replace('\n', '')
            links_list.append(link)

    result_list = list(set(links_list))  # eliminate duplicate links

    with open(new_file, "w") as file:
        for link in result_list:
            file.write(link + "\n")


def retrieve_last_seen_id(file_name):
    file = open(file_name, 'r')
    last_seen_id = int(file.read())  # ID of last status retweeted
    file.close()
    return last_seen_id


def store_last_seen_id(file_name, last_seen_id):
    file = open(file_name, 'w')
    file.write(str(last_seen_id))
    file.close()
    return


def load_links_to_post(file_name):
    links_list = list()
    with open(file_name, "r") as file:
        for line in file:
            link = line.replace('\n', '')
            links_list.append(link)
    return links_list


def store_links_to_post(links_list, index, file_name):
    links_list.pop(index)
    with open(file_name, "w") as file:
        for link in links_list:
            file.write(link + "\n")
    return