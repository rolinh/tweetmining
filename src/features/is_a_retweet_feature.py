from features import abstract_feature as af
import re

class IsARetweetFeature(af.AbstractFeature):

    def __repr__(self):
        return "<IsARetweetFeature>"

    def __str__(self):
        return "Is A Retweet Feature"

    def extract(self, tweet):
        is_a_retweet = False
        pattern      = re.compile('RT @.+: ')

        if pattern.match(tweet.text) != None:
            is_a_retweet = True
        return "is_a_retweet", is_a_retweet
