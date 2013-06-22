from twitter import tweet as t
from twitter import user as usr
from twitter import hashtags as h
from twitter import url as u
from twitter import user_mention as um
from twitter import entities as e

import json
import codecs
import re

def json_to_tweets_helper(data, bad_data):
    """Helper for the `json_to_tweets` function"""
    tweet_collection = []

    for tw in data['statuses']:
        # yay, some tweet do not have any user (dafuk?)
        if not 'user' in tw:
            continue

        if bad_data:
            screen_name = ''
            in_reply_to_status_id = \
                    in_reply_to_user_id =\
                    favorite_count = \
                    retweet_count = \
                    user_favorite_count = \
                    followers_count = \
                    friends_count = \
                    statuses_count = 0
            verified = False
        else:
            screen_name = tw['user']['screen_name']
            in_reply_to_status_id = tw['in_reply_to_status_id']
            in_reply_to_user_id = tw['in_reply_to_user_id']
            favorite_count = tw['favorite_count']
            retweet_count = tw['retweet_count']
            user_favorite_count = tw['user']['favourites_count']
            followers_count = tw['user']['followers_count']
            friends_count = tw['user']['friends_count']
            statuses_count = tw['user']['statuses_count']
            verified = tw['user']['verified']

        hashtags = []
        for hashtag in tw['entities']['hashtags']:
            hashtags.append(h.Hashtags(hashtag['text']))

        urls = []
        for url in tw['entities']['urls']:
            urls.append(u.Url(url['display_url']))

        user_mentions = []
        for user_mention in tw['entities']['user_mentions']:
            user_mentions.append(um.UserMention(
                                    user_mention['id'],
                                    user_mention['name'],
                                    user_mention['screen_name']))

        entities = e.Entities(hashtags, urls, user_mentions)

        user =  usr.User(tw['user']['id'],
                         screen_name,
                         user_favorite_count,
                         followers_count,
                         friends_count,
                         statuses_count,
                         verified)

        tweet = t.Tweet(tw['id'],
                        user,
                        tw['created_at'],
                        tw['text'],
                        entities,
                        in_reply_to_status_id,
                        in_reply_to_user_id,
                        favorite_count,
                        retweet_count)

        tweet_collection.append(tweet)

    return tweet_collection

def json_to_tweets(json_tweet_file, bad_data=False):
    """Map each json object to a Twitter object, returning a collection of
    tweets"""

    tweet_collection = []

    with codecs.open(json_tweet_file, 'r', 'utf-8') as f:
        json_list = f.readlines()

    for j in json_list:
        data = json.loads(j)
        tweet_collection += json_to_tweets_helper(data, bad_data)

    return tweet_collection

def tag_as_retweet(dataset):
    """Search retweet in a data set and return a dictionnary in which the key
    represent the ID of the original tweet and the value represent number of
    retweets"""

    rval = {}

    for tweet in dataset:
        m = re.search('^RT @(.+): (.*)$', tweet.text)

        if m == None:
            continue

        username = m.group(1)
        content  = m.group(2)

        for tmp in dataset:
            if tmp.user.screen_name != username:
                continue

            if tmp.text == content:
                if tmp.id in rval:
                    rval[str(tmp.id)] += 1
                else:
                    rval[str(tmp.id)] = 1


    return rval

def bool_as_label(boolean):
    """Convert boolean into a '1' or '0' string"""
    return '1' if boolean else '0'
