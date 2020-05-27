# HPlusBot - A transhumanist twitter bot!

This is the repository of the [HPlusBot in Twitter](https://twitter.com/HplusBot).
The bot account in Twitter follows transhumanist thinkers, associations, webpages, and the like; and tweets and retweets 
about transhumanism and future related stuff.

Table of Contents
=================

  * [What the bot does?](#what-the-bot-does)
  * [Used modules](#used-modules)
  * [Things to consider](#things-to-consider)
    * [Issues with Heroku deployment](#issues-with-heroku-deployment)
    * [Keywords and Hashtags](#keywords-and-hashtags)
    * [Ratio of likes of a tweet to be retweeted](#ratio-of-likes-of-a-tweet-to-be-retweeted)
    * [Other notes](#other-notes)
    * [Issues with naming convention](#issues-with-naming-convention)

## What the bot does?

1. Periodically retweets recents tweets of the followed users that:
    - reach a certain number of likes
    - matches one or more keywords or hashtags
2. Tweets scrapped data (titles and urls) from:
    - Random pages from [H+Pedia](https://hpluspedia.org/)
    - Articles from The New York Times
    - Urls shared in subreeddits as:
        - [/r/Transhumanism](https://www.reddit.com/r/transhumanism/)
        - [/r/Transhuman](https://www.reddit.com/r/transhuman/)
        - [/r/Singularity](https://www.reddit.com/r/singularity/)
        - [/r/Futurology](https://www.reddit.com/r/futurology/)

## Used modules:

The bot utilizes the [Twitter](https://developer.twitter.com/en), [The New York Times](https://developer.nytimes.com/), 
and [Reddit APIs](https://www.reddit.com/dev/api).
The bot is built in Python employing the following libraries:
  - [Tweepy](http://docs.tweepy.org/en/latest/api.html)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - [Python Reddit Api Wrapper (PRAW)](https://praw.readthedocs.io/en/latest/)
  - [Advanced Python Scheduler (APScheduler)](https://apscheduler.readthedocs.io/en/stable/)
  - [Requests](https://requests.readthedocs.io/en/master/)
  
  
## Things to consider:
 
#### Issues with Heroku deployment:
 
The "Last_Tweet_ID.txt" file was intended to be used as a starting point in each iteration of the retweet function, in 
which the ID it contains is renewed at the end of each iteration (the ID of the last tweet retweeted is written). 
This is done this way to avoid going all the way through a lot of tweets in an user timeline (from x to y; 
ej: from a tweet of 1st March all the way to the last one in 31st of March). So, the file should change in each iteration 
and this should be so indefinitely.

In case of "Links_to_post.txt", this file contains all links that directs to New York Times website. As the links are 
tweeted randomly, the scripts deletes them to ensure that there are no duplicated tweets with the same link. 

Both of the files names, in Heroku, have very limited use and do not work as intended because changes made directly to the 
filesystem on Heroku dynos will be lost whenever the dyno restarts; the content of the file are restored in each cycle, 
they will be as the last push to Heroku.

This happens frequently: Dynos are restarted (cycled) at least once per day to help maintain the health of
applications running on Heroku. Any changes to the local filesystem will be deleted. The cycling happens once every 24
hours. Check out: https://stackoverflow.com/questions/42194043/can-heroku-edit-files

With "Last_Tweet_ID.txt", to avoid in some way going all the way through a lot of tweets in an user timeline 
(as it was intended originally), once in a while is needed a manual overwriting of the file and push to heroku master.
One can simply forget about "Links_to_post.txt", but ideally should be a way to make things work as intended. 

* TODO:
The implementation of a database that stores the tweet ID  and the NYT links can avoid the deletion of changed files 
when the dyno restart. This is the next step of the HPlus Bot proyect.
 
#### Keywords and Hashtags

The keywords and hashtags are the elements we use to filter all the tweets and the NYT articles and select only those that
comply with the criteria. They are very similar to each other, but while in Twitter we use both, to search for articles
we use only the keywords. Also, there is a lot of redundancy because we have in mind the singular and plural use of the
words.

- KEYWORDS

| -isms | Technologies | Nouns | Verbs |
| --- | --- | --- | --- |
| 'futurism' | 'ai' | 'cyborg' | 'enhance' |
| 'posthumanism' | 'biohacking' | 'cyborgs' | performance-enhancing' |
| 'transhumanism' | 'biotechnology' | 'futurist' | 're-engineering' |
|  | 'crispr' | 'immortality' |  |
|  | 'cybernetics' | 'posthumanist' |  |
|  | 'nanotechnology' | 'robots' |  |
|  |  | 'singularity' |  |
|  |  | 'techno-utopias' |  |
|  |  | 'transhuman' |  |
|  |  | 'transhumans' |  |
|  |  | 'transhumanist' |  |
|  |  | 'transhumanists' |  |

- HASHTAGS

| -isms | Technologies | Nouns | Verbs |
| --- | --- | --- | --- |
| '#futurism' | '#agi' | '#augmentation' | '#biohacking' |
| '#posthumanism' | '#ai' | '#bionic' |  |
| '#transhumanism' | '#artificialintelligence' | '#cyborg' |  |
|  | '#augmentedreality' | '#genetics' |  |
|  | '#crispr' | '#longevity' |  |
|  | '#cybernetics' | '#machineintelligence' |  |
|  | '#nanotech' | '#posthumanist' |  |
|  |  '#nanotechnology' | '#singularity' |  |
|  |  '#robotics' | '#transhumanist' |  |
|  |  '#nanotechnology' |  |  |

 
#### Ratio of likes of a tweet to be retweeted

The ratio_of_likes() function was called the 20/03/2020
The chosen id tweet from 01/03/2020 (to start the search) was: 1233972953169252352 [from Last_ID_Tweet.txt]
The bot checked 3277 tweets (no rt) from 48 Followings.
Only 189 tweets complied with the criteria of keywords and hashtags.

|   | [500>>] | [50-499] | [0-49] |
| --- | --- | --- | --- |
| Quantity | 1 | 10 | 178
| Total likes | 887 | 737 | 1385
| Ratio | 887.0  | 73.7 | 7.78

As the quantity of tweets with more than 49 likes is almost trivial, the chosen ratio from which decide if the status is
 going to be retweeted by the bot is: 7 likes.
 
#### Other notes:
  
  - The original Last_Tweet_ID was: 1246479431750672385 (a tweet from 4/4/20 by @zoltan_istvan)
  
  - The search of gather_data() in NYT.py resulted in a total of 866 links:

| Query | Number of Links |
| --- | --- |
| TRANSHUMANISM | 12 |
| CYBORG | 132 |
| POSTHUMANISM | 14 |
| FUTURISM | 190 |
| TECHNO-UTOPIAS | 10 |
| ARTIFICIAL INTELLIGENCE | 255 |
| GENETIC MANIPULATION | 54 |
| NANOTECHNOLOGY | 211 |

- The list of links from NYT was subject to removing duplicates links and checking manually all the links (as even if 
them complied to the searching criteria of the code, some links weren´t related to the actual content we want to post, 
i.e. some are about art, old or uninteresting news, etc.). The final list consist of *342 links total*.

 
#### Issues with naming convention:
 
I made mistakes with the naming of the files; I did not respect the convention of naming files with all characters in
lowercase. But I can´t change the filenames without losing the changes history. In the future I´ll keep more in mind 
the PEP8 convention.

# Next things to do:

- Make a Sentiment Analysis (check https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/)
- Implement a database where to store all the links to NYT and the last_id_tweet.
- Implement a database where to dump data from the tweets that the bote made and make some data science analysis