import Setup
import time
from datetime import date


SUBREDDITS = ['Transhuman', 'Transhumanism', 'Singularity', 'Futurology']


def start_stream(api):
    """
    This functions streams the submissions of four subreddits: /r/Transhuman, /r/Transhumanism, /r/Singularity, and
    /r/ Futurology. At first grabs a wave of recent submissions, which can be a lot of them. After that wave, it grabs
    at real time the submissions. The functions scrapes the title of the submission and the url assocciated (as long
    the URL the submission links to is not a selfpost permalink ). The scrapped data is formatted and tweeted.
    A sleep time of 5 minutes is added after the tweet to avoid flooding the timeline and avoid reaching the api limit
    rate. Also, the function only tweets if the current day is even. This is needed to avoid flooding the timeline and
    tweeting duplicated status as the heroku slug resets every 24 hs.
    """
    reddit = Setup.setup_reddit()
    subreddits = reddit.subreddit('+'.join(SUBREDDITS))

    for submission in subreddits.stream.submissions():

        if date.today().day % 2 == 0:  # As the heroku slug resets every 24hs, to avoid a wave of repeated tweets from
            # this stream, the function tweets only every even day.

            url = submission.url
            if 'www.reddit.com' not in url and 'i.redd.it' not in url:
                if len(submission.title) > 100:
                    title = submission.title[:100] + '...'  # Needed in case it exceeds the tweeet character limit
                else:
                    title = submission.title
                try:
                    print("Tweeting data from Reddit")
                    api.update_status(status=f"Check out \"{title}\" at: {url}")
                except:
                    print("No tweeting a duplicated status")
                    continue
                time.sleep(300)  # sleeps for five minutes to avoid twitter api and reddit api limit rate
                # also to avoid flooding twitter timeline
