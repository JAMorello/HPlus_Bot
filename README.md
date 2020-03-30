# HPlusBot - A transhumanist twitter bot!

This is the repository of the [HPlusBot in Twitter](https://twitter.com/HplusBot).
This bot tweets and retweets about transhumanism and future related stuff.
The bot account in Twitter follows transhumanist thinkers, associations, webpages, and the like.

## What the bot does?

1. Periodically retweets recents post of the followed users that:
    - reach a certain number of likes
    - matches one or more keywords or hashtags (related to the )
2. Tweets scrapped data (titles and urls) from:
    - Random pages from [H+Pedia](https://hpluspedia.org/)
    - Articles from [The New York Times API](https://developer.nytimes.com/)
    - Urls shared in subreeddits as:
        - [/r/Transhumanism](https://www.reddit.com/r/transhumanism/)
        - [/r/Transhuman](https://www.reddit.com/r/transhuman/)
        - [/r/Singularity](https://www.reddit.com/r/singularity/)
        - [/r/Futurology](https://www.reddit.com/r/futurology/)

The bot applies the REST functionalities of the Twitter api and NYT api, and the streaming one of the Reddit api.
The bot is built in Python employing the following libraries:
  - Tweepy
  - Beautiful Soup
  - Python Reddit Api Wrapper (PRAW)
  - Advanced Python Scheduler (APScheduler)
  - Requests