import tweepy
# TWEEPY API REFERENCE: http://docs.tweepy.org/en/latest/api.html
import os

KEYWORDS = ["transhumanism", "transhumanist", "transhumanists", "ai", "robots",
            "futurism", "cybernetics", "cyborg", "cyborgs", "nanotechnology", "biohacking",
            "crispr", "posthumanism", "posthumanist"]
HASHTAGS = ["#transhumanism", "#transhumanist", "#ai", "#robotics", '#artificialintelligence',
            "#genetics",  "#futurism", "#cybernetics", "#cyborg", "#nanotechnology", "#biohacking",
            "#crispr", "#machineintelligence", "#posthumanism", "#augmentedreality", "#nanotech ",
            "#agi", "#singularity", "#posthumanist", "#longevity", "#augmentation", "#bionic"]

def setup():
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
