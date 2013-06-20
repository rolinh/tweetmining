from twitter import tweet as t
from twitter import user as usr
from twitter import hashtags as h
from twitter import url as u
from twitter import user_mention as um
from twitter import entities as e

import json
import codecs
import re

def json_to_tweets(json_tweet_file):
    """Map each json object to a Twitter object, returning a collection of
    tweets"""

    tweet_collection = []

    with codecs.open(json_tweet_file, 'r', 'utf-8') as f:
        data = json.load(f)

    for tw in data['statuses']:
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

        user =  usr.User(tw['user']['id'], tw['user']['screen_name'])

        tweet = t.Tweet(tw['id'],
                        user,
                        tw['created_at'],
                        tw['text'],
                        entities,
                        0,
                        0)

        tweet_collection.append(tweet)

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
