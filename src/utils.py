from twitter import tweet as t

import json

def json_to_tweets(json_tweet_file):
    """Map each json object to a Twitter object, returning a collection of
    tweets"""

    tweet_collection = []

    with open(json_tweet_file) as f:
        data = json.load(f)

    for tw in data['statuses']:
        tweet = t.Tweet(tw['id'],
                        tw['user']['id'],
                        tw['created_at'],
                        tw['text'],
                        tw['in_reply_to_status_id'],
                        tw['in_reply_to_user_id'])
        tweet_collection.append(tweet)

    return tweet_collection


