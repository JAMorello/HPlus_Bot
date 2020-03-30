import tweepy
# TWEEPY API REFERENCE: http://docs.tweepy.org/en/latest/api.html
import praw
# CHECK REDDIT API ---> https://www.reddit.com/dev/api
# PRAW (Python Reddit API Wrapper) documentation: https://praw.readthedocs.io/en/latest/
import os

LIKES_TO_RETWEET = 7

KEYWORDS = ['ai', 'biohacking', 'biotechnology','crispr', 'cybernetics', 'cyborg', 'cyborgs', 'enhance', 'futurism',
            'futurist', 'immortality', 'nanotechnology', 'performance-enhancing', 'posthumanism', 'posthumanist',
            're-engineering', 'robots', 'singularity', 'techno-utopias', 'transhuman', 'transhumans', 'transhumanism',
            'transhumanist', 'transhumanists']
HASHTAGS = ['#agi', '#ai', '#artificialintelligence', '#augmentation', '#augmentedreality', '#biohacking', '#bionic',
            '#crispr', '#cybernetics', '#cyborg', '#futurism', '#genetics', '#longevity', '#machineintelligence',
            '#nanotech ', '#nanotechnology', '#posthumanism', '#posthumanist', '#robotics', '#singularity',
            '#transhumanism', '#transhumanist']

NYT_API_KEY = os.getenv('NYT_API_KEY')
# Check https://developer.nytimes.com/


def setup_twitter():
    # Authenticate to Twitter and passing keys from environment variables
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
    # Construct the API instance.
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)  # print a message and wait if the rate limit is exceeded

    # Test authentication
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api


def setup_reddit():
    reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                         client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                         user_agent='python:HPlus_Bot:v1 (by /u/KamizakeRobot)')
    return reddit
