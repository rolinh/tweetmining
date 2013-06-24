from features import abstract_feature as af

class FriendsCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FriendsCountFeature>"

    def __str__(self):
        return "Friends Count Feature"

    def extract(self, tweet):
        return "friends_count", tweet.user.friends_count

