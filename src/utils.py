from twitter import tweet as t
from twitter import hashtags as h
from twitter import url as u
from twitter import user_mention as um
from twitter import entities as e

import json

def json_to_tweets(json_tweet_file):
    """Map each json object to a Twitter object, returning a collection of
    tweets"""

    tweet_collection = []

    with open(json_tweet_file) as f:
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

        tweet = t.Tweet(tw['id'],
                        tw['user']['id'],
                        tw['created_at'],
                        tw['text'],
                        entities,
                        0,
                        0)

        tweet_collection.append(tweet)

    return tweet_collection


