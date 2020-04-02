import Setup
import tweepy
import time

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
            try:
                print("Tweeting data from Reddit")
                api.update_status(status=f"Check out \"{title}\" at: {url}")
            except:
                print("No tweeting a duplicated status")
                continue
            time.sleep(60)  # sleeps for one minute to avoid twitter api and reddit api limit rate
            # also to avoid flooding twitter timeline
