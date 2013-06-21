from features import abstract_feature as af

class HasUrlFeature(af.AbstractFeature):

    def __repr__(self):
        return "<HasUrlFeature>"

    def __str__(self):
        return "Has URL Feature"

    def extract(self, tweet):
        b = True if len(tweet.entities.urls) > 0 else False
        return "has_url", b
