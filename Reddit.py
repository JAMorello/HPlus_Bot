import Setup
import time
from Bot_REST import post_tweet

SUBREDDITS = ['Transhuman', 'Transhumanism', 'Singularity', 'Futurology']


def start_stream(api):
    reddit = Setup.setup_reddit()
    subreddits = reddit.subreddit('+'.join(SUBREDDITS))

    for submission in subreddits.stream.submissions():
        url = submission.url
        if 'www.reddit.com' not in url and 'i.redd.it' not in url:
            if len(submission.title) > 100:
                title = submission.title[:100] + '...'
            else:
                title = submission.title
            print("Tweeting data from Reddit")
            post_tweet(api, f"Check out \"{title}\" at: {url}")
            time.sleep(60)  # sleeps for one minute to avoid twitter api and reddit api limit rate
            # also to avoid flooding twitter timeline
