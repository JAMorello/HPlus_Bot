import Setup
import tweepy
import json


def check_tweets(api, username):
    """
    With this function we can make sure that the user passed as parameter has made tweets of retweets
    about the subjects of our interest (passed here as the Keywords and Hashtags in Setup.py). A minimum of x
    tweets (in this case, 2) must be reached for the user be eligible to be followed.
    """
    tweets_list = api.user_timeline(username)  # The variable holds an object that contains the last 20 tweets in their
    # timeline
    counter = 0

    for tweet in tweets_list:
        # The info that the API gave us about the user is messy.
        # We need a json to properly access the data.
        json_str = json.dumps(tweet._json)  # convert to string
        parsed = json.loads(json_str)  # deserialise string into python object

        tweet_text = parsed["text"].lower().split()  # A list that contains all the words of the tweet

        if any(elem in Setup.KEYWORDS for elem in tweet_text) or \
           any(elem in Setup.HASHTAGS for elem in tweet_text):
            counter += 1

    # At least 2 recent tweets must match our criteria of keywords and hashtags
    return True if counter >= 2 else False


def search_for_users(api):
    """
    This functions search for the first 200 users in Twitter (in the same
    way as the Find People button on Twitter.com. The  used is: the user must have
    at least 1000 followers and the bot account does not follow the user. Then, if
    that criteria is met, then the check_tweets() is called. The info of users that
    pass the check (their screen_name, number of followers, and profile description)
    are dumped in a dictionary and after that in a list. The result that appears in the
    terminal is a filtered     list of users that possibly could be of our interested
    (we have to check manually in the webpage).

    [The first time calling this function, the output was of more or less 10% of number of items]
    """

    user_list = tweepy.Cursor(api.search_users, q='transhumanism').items(200)
    users_data = [] # Here we are going to store the users information

    for user in user_list:
        # The object that the API give us about the user is messy.
        # We need a json to properly access the data.
        json_str = json.dumps(user._json)  # convert to string
        parsed = json.loads(json_str)  # deserialise string into python object

        try:
            if parsed["followers_count"] > 1000 and not parsed["following"]:
                if check_tweets(api, parsed["screen_name"]):
                    user = {
                        "name": parsed["screen_name"],
                        "followers": parsed["followers_count"],
                        "description": parsed["description"]
                    }
                    users_data.append(user)
                    print("Data fetched.")
        except Exception:  # An error can occur if the user has protected tweets.
            print(f"Failed to run the command on ", parsed["screen_name"], "skipping...\n")
            continue

    print("Done\n")
    for user in users_data:
        print(user, "\n")


if __name__ == "__main__":
    api = Setup.setup()
    search_for_users(api)