from features import abstract_feature as af

import nltk

class TweetLengthFeature(af.AbstractFeature):

    def __repr__(self):
        return "<TweetLengthFeature>"

    def __str__(self):
        return "Tweet Length Feature"

    def extract(self, tweet):
        return "tweet_length", len(nltk.word_tokenize(tweet.text))
