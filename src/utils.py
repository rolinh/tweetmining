from twitter import tweet as t
from twitter import user as usr
from twitter import hashtags as h
from twitter import url as u
from twitter import user_mention as um
from twitter import entities as e

from scipy import stats

import json
import codecs
import re
import numpy
import math
import nltk
import datetime

import words_processing as wp

def words_occ_to_dict(words_occ_file):
    """Parses a file of words with their occurrency where each line is in the
    form word:occurrency and insert them into a dictionary. The dictionary is
    then returned."""
    d = {}
    f =  codecs.open(words_occ_file, 'r', 'utf-8')
    for line in f:
        k,v = line.split(':')
        d[k] = int(v)
    f.close()
    return d

def words_occ_to_tf(d):
    """Returns a numpy array of the TF of each word from the dictionnary."""
    d_tf = {}
    ks = d.keys()
    vs = wp.tf(d)

    for i,v in enumerate(ks):
        d_tf[v] = vs[0,i]

    return d_tf

def words_occ_to_tfidf(d):
    """Returns a numpy array of the TF-IDF of each word from the dictionnary."""
    d_tf_idf = {}
    ks = d.keys()
    vs = wp.tf_idf(d)

    for i,v in enumerate(ks):
        d_tf_idf[v] = vs[0,i]

    return d_tf_idf

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

def mcnemar(contingency_table):
    """Perform the McNemar test and return the Chi-square value and
    the p-value.

    The contingency must have the following format (array of array):

    Let A and B be the two classifiers we want to compare.

             |                   |                    |
             |         F         |         T          |
             |                   |                    |
    ---------------------------------------------------
             |       # of        | # of misclssified  |
        F    |   misclassified   | by A and # of well |
             |    by A and B     | classified by B    |
    ---------------------------------------------------
             |# of wellclassified|       # of         |
        T    |by A and           |   wellclassified   |
             |misclassified by B |     by A and B     |
    ---------------------------------------------------
    """

    ff = contingency_table[0][0]
    ft = contingency_table[0][1]
    tf = contingency_table[1][0]
    tt = contingency_table[1][1]

    if ft + tf == 0:
        chi_square = 0
    else:
        chi_square = float((abs(ft-tf)-1)**2)/float(ft+tf)
    p_value    = 1 - stats.chi2.cdf(chi_square, 1, 0)

    return chi_square, p_value

def entropy(labels):
    """Compute the entropy of the given labels."""
    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(l) for l in freqdist]
    return -sum([p * math.log(p, 2) for p in probs])

def format_tweet_date(tweet_date):
    """Format a date in the format found in a tweet in a standard date format"""
    d = tweet_date.split(' ')
    formatted_date = "%s %s %s" % (d[1], d[2], d[5])
    return datetime.datetime.strptime(formatted_date, "%b %d %Y")

def tweets_date_range(dataset):
    """Return the number of days beetweet the oldest and the newest tweet from
    the gived tweets `dataset`"""

    oldest = newest = format_tweet_date(dataset[0].created_at)

    for tweet in dataset:
        d = format_tweet_date(tweet.created_at)
        if d < oldest:
            oldest = d
        if d > newest:
            newest = d

    return oldest, newest
