from features import abstract_feature as af

class HashtagCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<HashtagCountFeature>"

    def __str__(self):
        return "Hashtag Count Feature"

    def extract(self, tweet):
        return "hashtag_count_feature", len(tweet.entities.hashtags)
