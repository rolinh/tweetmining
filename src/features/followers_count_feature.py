from features import abstract_feature as af

class FollowersCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FollowersCountFeature>"

    def __str__(self):
        return "Followers Count Feature"

    def extract(self, tweet):
        return "followers_count", tweet.user.followers_count

