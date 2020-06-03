import time
import tweepy

import Setup
from hplusbot_database import insert_user_data, insert_tweet_data
from twitterbot_utilities import to_json


class MyStreamListener(tweepy.StreamListener):
    def on_connect(self):
        print("Stream Listener Connected!")

    def on_status(self, status):
        parsed_status = to_json(status)
        text = parsed_status['text']
        if not text.startswith("RT @"):
            tweet_id_str = parsed_status['id_str']
            try:
                tweet_text = parsed_status['extended_tweet']['full_text']
            except:
                tweet_text = parsed_status['text']
            tweet_created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(parsed_status['created_at'],
                                                                                  '%a %b %d %H:%M:%S +0000 %Y'))
            if parsed_status['is_quote_status']:
                tweet_quoted = parsed_status["quoted_status_id_str"]
            else:
                tweet_quoted = ""

            user_id_str = parsed_status['user']['id_str']
            user_screen_name = parsed_status['user']['screen_name']
            user_description = parsed_status['user']['description']
            user_location = parsed_status['user']['location']
            user_followers = parsed_status['user']['followers_count']
            user_friends = parsed_status['user']['friends_count']
            user_statuses = parsed_status['user']['statuses_count']
            user_favourites = parsed_status['user']['favourites_count']

            insert_user_data(user_id_str, user_screen_name, user_description, user_location, user_followers,
                             user_friends, user_statuses, user_favourites)
            insert_tweet_data(tweet_id_str, tweet_text, tweet_created_time, tweet_quoted, user_id_str)

            print("Tweet and user inserted into database")

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            print("Encountered streaming error (", status_code, ")")
            return False
        # returning non-False reconnects the stream, with backoff.


def start_twitter_stream(api):
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)

    while True:
        try:
            tags = ['transhumanism']
            my_stream.filter(track=tags)
        except:
            continue


# Start the streaming
api = Setup.setup_twitter()
start_twitter_stream(api)
