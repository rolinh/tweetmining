# coding: utf-8
import words_processing as wp
import datetime

def tf_freq_max(tweet, word_frequencies):
    """Return the maximum frequency of the word that has the max frequency in
    the `tweet`"""
    freq_max = 0
    tokens = wp.filter_tweet_words(tweet)
    for word in tokens:
        v = word_frequencies[word]
        if v > freq_max:
            freq_max = v
    return freq_max

def delta_date(from_str_date):
    """Calculate the delta (# of days) between a given date and today.
    The `from_str_date` must have the following format :
    "Sun Sep 16 03:24:58 +0000 2012" """

    d = from_str_date.split(' ')
    formatted_date = "%s %s %s" % (d[1], d[2], d[5])

    today = datetime.date.today()
    date1 = datetime.datetime(today.year, today.month, today.day)
    date2 = datetime.datetime.strptime(formatted_date, "%b %d %Y")
    delta = date2-date1

    return abs(delta.days)
