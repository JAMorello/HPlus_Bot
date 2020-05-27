import Setup
import tweepy
import time
import Reddit
import HPlus_Pedia
import NYT
from twitterbot_utilities import to_json, word_list, retrieve_last_seen_id, store_last_seen_id
from apscheduler.schedulers.background import BackgroundScheduler

LAST_ID_FILE = "data/Last_Tweet_ID.txt"
# This file presents some problems when deployed to Heroku. See documentation.
BOT_USERNAME = "HPlusBot"
LIKES_TO_RETWEET = 7


def wiki_post_tweet(api):
    api.update_status(status=HPlus_Pedia.random_page())
    return


def nyt_post_tweet(api):
    api.update_status(status=NYT.scrapper())
    return


def retweet(api):
    """
    The function retweets all the tweets (no retweets) of the users that the bot follows.
    Specifically retweets those who comply to the criteria of keywords and/or hashtags, have a certain minimum number
    of likes, and were posted after a certain tweet (that is stored in Last_Tweet_ID.txt). At the end, the ID of the
    last tweet retweeted is stored in the .txt to serve as the starting point of the next call to the function.
    """
    last_retweet_id = retrieve_last_seen_id(LAST_ID_FILE)
    most_recent_status_id = last_retweet_id
    users_followed = api.friends_ids(screen_name=BOT_USERNAME)  # List of IDs of users that the bot follows

    for user in users_followed:

        tweets_list = tweepy.Cursor(api.user_timeline, id=user, tweet_mode='extended',
                                    since_id=last_retweet_id).items()

        for tweet in tweets_list:

            parsed_tweet = to_json(tweet)
            tweet_text = word_list(parsed_tweet["full_text"])

            if not tweet_text[0] == "rt" and parsed_tweet["favorite_count"] >= LIKES_TO_RETWEET:
                # Checks if the status is not a retweet and if it has at least x likes required

                if any(elem in Setup.HASHTAGS for elem in tweet_text) or \
                        any(elem in Setup.KEYWORDS for elem in tweet_text):
                    # Checks if the tweet matches the criteria of keywords or hashtags (at least one element of any
                    # of those)

                    try:
                        api.retweet(id=parsed_tweet["id"])
                        print(f'Retweet: {parsed_tweet["id"]}')
                    except:
                        print("Already retweeted")

                    time.sleep(5)
                    # If there is a lot of status to go through, it´s better to avoid the api limit rate with sleep.

                    if parsed_tweet["id"] > most_recent_status_id:
                        most_recent_status_id = parsed_tweet["id"]

    print("Retweeting done!")
    store_last_seen_id(LAST_ID_FILE, most_recent_status_id)


if __name__ == "__main__":
    api = Setup.setup_twitter()

    # As the scheduler is not the only thing running in our process (we also use the streaming from Reddit),
    # we want the scheduler to run in the background inside the script along other functionalities.
    scheduler = BackgroundScheduler()

    scheduler.add_job(retweet, 'interval', args=[api], hours=3)
    scheduler.add_job(wiki_post_tweet, 'interval', args=[api], hours=5)
    scheduler.add_job(nyt_post_tweet, 'interval', args=[api], hours=12)
    scheduler.start()

    Reddit.start_stream(api)

#
#
# WARNING!
# OLD METHODS AHEAD!!
# ONLY FOR REFERENCE, NOT IN USE ACTUALLY
#
#


def ratio_of_likes(api):
    """
    The purpose of this function is to determinate a certain number of likes that is going to be used as a criteria
    that the tweets need to match to be retweeted. To do so, the function iterates trough the tweets of the users
    that the bot follows and gets the likes of those tweets. The function selects only the tweets that were
    posted after a certain tweet (that is stored in Last_Tweet_ID.txt) and specifically those who comply to the criteria
    of keywords and/or hashtags.
    Two dictionaries store the data: one for the number of tweets that have between 0-49, between 50-499, and more
    than 500 likes; and another for the total of likes between those ranges. The function then prints the ranges,
    number of tweets in each range, the total of likes in each range, and the ratio
    (total of likes / number of tweets in that range).
    """

    total = {
        "500<<": 0,
        "50-499": 0,
        "0-49": 0
    }
    quantity = {
        "500<<": 0,
        "50-499": 0,
        "0-49": 0
    }
    total_tweets = 0

    last_retweet_id = retrieve_last_seen_id(LAST_ID_FILE)

    users_followed = api.friends_ids(screen_name="HPlusBot")   # List of IDs of users that the bot follows

    for user in users_followed:

        tweets_list = tweepy.Cursor(api.user_timeline, id=user, tweet_mode='extended',
                                    since_id=last_retweet_id).items()

        for tweet in tweets_list:

            parsed = to_json(tweet)
            total_tweets += 1

            tweet_text = word_list(parsed["full_text"])

            if not tweet_text[0] == "rt":  # Checks if the status is not a retweet

                if any(elem in Setup.HASHTAGS for elem in tweet_text) or \
                        any(elem in Setup.KEYWORDS for elem in tweet_text):

                    if parsed["favorite_count"] >= 500:
                        total["500<<"] += parsed["favorite_count"]
                        quantity["500<<"] += 1
                    elif parsed["favorite_count"] >= 50:
                        total["50-499"] += parsed["favorite_count"]
                        quantity["50-499"] += 1
                    else:
                        total["0-49"] += parsed["favorite_count"]
                        quantity["0-49"] += 1
                    print("Done ", total_tweets, parsed["user"]["screen_name"])

    print(total_tweets)

    if quantity["500<<"] > 0:
        print("500>> = ", quantity["500<<"])
        print("Total = ", total["500<<"])
        print("Ratio = ", total["500<<"] / quantity["500<<"], "\n")

    if quantity["50-499"] > 0:
        print("50-499 = ", quantity["50-499"])
        print("Total = ", total["50-499"])
        print("Ratio = ", total["50-499"] / quantity["50-499"], "\n")

    if quantity["0-49"] > 0:
        print("0-49 = ", quantity["0-49"])
        print("Total = ", total["0-49"])
        print("Ratio = ", total["0-49"] / quantity["0-49"], "\n")


def check_recent_tweets(api, username):
    """
    With this function we can make sure that the user passed as parameter has made tweets or retweets
    about the subjects of our interest (passed here as the Keywords and Hashtags in Setup.py). A minimum of x
    tweets (in this case, 2) must be reached for the user be eligible to be followed.
    """
    tweets_list = api.user_timeline(username)  # The variable holds an object that contains the last 20 tweets in their
    # timeline
    counter = 0

    for tweet in tweets_list:
        # The info that the API gave us about the user is messy.
        # We need a json to properly access the data.
        parsed = to_json(tweet)

        tweet_text = word_list(parsed["text"])  # A list that contains all the words of the tweet

        if any(elem in Setup.KEYWORDS for elem in tweet_text) or \
                any(elem in Setup.HASHTAGS for elem in tweet_text):
            counter += 1

    # At least 2 recent tweets must match our criteria of keywords and hashtags
    return True if counter >= 2 else False


def search_for_users(api):
    """
    This functions search for the first 200 users in Twitter (in the same
    way as the Find People button on Twitter.com) using the query "transhumanism".
    The criteria used is: the user must have at least 1000 followers and the bot account
    does not follow the user. Then, if that criteria is met, then the check_tweets() is called.
    The info of users that pass the check (their screen_name, number of followers, and profile
    description) are dumped in a dictionary and after that in a list. The result that appears in
    the terminal is a filtered list of users that possibly could be of our interested
    (we have to check manually in the webpage).

    [The first time calling this function, the output was of more or less 10% of number of items]
    """

    user_list = tweepy.Cursor(api.search_users, q='transhumanism').items(200)
    users_data = []  # Here we are going to store the users information

    for user in user_list:
        parsed = to_json(user)

        try:
            if parsed["followers_count"] > 1000 and not parsed["following"]:
                if check_recent_tweets(api, parsed["screen_name"]):
                    user = {
                        "name": parsed["screen_name"],
                        "followers": parsed["followers_count"],
                        "description": parsed["description"]
                    }
                    users_data.append(user)
                    print("Data fetched.")
        except:  # An error can occur if the user has protected tweets.
            print(f"Failed to run the command on ", parsed["screen_name"], "skipping...\n")
            continue

    print("Done\n")
    for user in users_data:
        print(user, "\n")
