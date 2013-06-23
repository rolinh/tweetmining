from features import abstract_feature as af

class StatusesCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<StatusesCountFeature>"

    def __str__(self):
        return "Statuses Count Feature"

    def extract(self, tweet):
        return "statuses_count", tweet.user.statuses_count
