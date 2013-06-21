from features import abstract_feature as af

class StatusesFeature(af.AbstractFeature):

    def __repr__(self):
        return "<StatusesFeature>"

    def __str__(self):
        return "StatusesFeature"

    def extract(self, tweet):
        return "statuses", tweet.user.statuses_count
