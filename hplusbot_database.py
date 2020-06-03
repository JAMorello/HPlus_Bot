import os
import psycopg2


def connect_database():
    db = psycopg2.connect(host='localhost',
                             user='postgres',
                             password=os.getenv('DB_PASSWORD'),
                             database='hplusbot')
    return db


def insert_user_data(user_id_str, screen_name, description, location, followers, friends, statuses, favourites):
    my_db = connect_database()
    cur = my_db.cursor()

    query = """INSERT INTO twitter_user (
                   user_id_str,
                   user_screen_name,
                   description,
                   location,
                   followers,
                   friends,
                   statuses,
                   favourites)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (user_id_str) 
                   DO UPDATE SET user_screen_name = EXCLUDED.user_screen_name,
                   description = EXCLUDED.description,
                   location = EXCLUDED.location,
                   followers = EXCLUDED.followers,
                   friends = EXCLUDED.friends,
                   statuses = EXCLUDED.statuses,
                   favourites = EXCLUDED.favourites;
        """
    cur.execute(query, (user_id_str, screen_name, description, location, followers, friends, statuses, favourites))
    my_db.commit()
    cur.close()


def insert_tweet_data(tweet_id_str, text, created_time, tweet_quoted, user_id_str):
    my_db = connect_database()
    cur = my_db.cursor()
    query = """INSERT INTO twitter_tweet (
                       tweet_id_str,
                       text,
                       created_at,
                       tweet_quoted,
                       user_id_str
                       )
                       VALUES (%s, %s, %s, %s, %s);
            """
    cur.execute(query, (tweet_id_str, text, created_time, tweet_quoted, user_id_str))
    my_db.commit()
    cur.close()


def db_get_last_tweet_id():
    my_db = connect_database()
    cur = my_db.cursor()
    query = "SELECT last_tweet_id FROM tweet_id WHERE id = 1"
    cur.execute(query)
    result = cur.fetchall()
    tweet_id = int(result[0][0])
    my_db.commit()
    cur.close()

    return tweet_id


def db_store_last_tweet_id(most_recent_status_id):
    my_db = connect_database()
    cur = my_db.cursor()
    query = """INSERT INTO tweet_id (last_tweet_id) 
               VALUES (%s)
               WHERE id = 1"""
    cur.execute(query, (most_recent_status_id,))
    my_db.commit()
    cur.close()


def db_num_nyt_links():
    my_db = connect_database()
    cur = my_db.cursor()
    query = "SELECT COUNT(*) FROM nyt_links;"
    cur.execute(query)
    result = cur.fetchall()
    num_links = result[0][0]
    my_db.commit()
    cur.close()
    return num_links


def db_get_nyt_link(index):
    my_db = connect_database()
    cur = my_db.cursor()
    query = "SELECT link FROM nyt_links WHERE id = %s"
    cur.execute(query, (index,))
    result = cur.fetchall()
    link = result[0][0]
    my_db.commit()
    cur.close()

    return link

# TODO: https://towardsdatascience.com/streaming-twitter-data-into-a-mysql-database-d62a02b050d6
# https://towardsdatascience.com/storing-tweets-in-a-relational-database-d2e4e76465b2
# https://www.dataquest.io/blog/streaming-data-python
