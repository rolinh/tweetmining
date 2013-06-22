# coding: utf-8
import words_processing as wp

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

