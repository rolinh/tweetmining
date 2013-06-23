from features import abstract_feature as af
from features import features_helper as helper

class TweetAgeFeature(af.AbstractFeature):

    def __repr__(self):
        return "<TweetAgeFeature>"

    def __str__(self):
        return "Tweet Age Feature"

    def extract(self, tweet):
        days = helper.delta_date(tweet.created_at)
        return "tweet_age", days
