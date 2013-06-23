from features import abstract_feature as af

class HashtagPopularityFeature(af.AbstractFeature):

    def __repr__(self):
        return "<HashtagPopularityFeature>"

    def __str__(self):
        return "Hashtag Popularity Feature"

    def extract(self, tweet):
        raise(NotImplementedError, "Not implemented yet!")
