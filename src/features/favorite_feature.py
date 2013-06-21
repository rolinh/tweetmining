from features import abstract_feature as af

class FollowersFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FollowersFeature>"

    def __str__(self):
        return "Followers Feature"

    def extract(self, tweet):
        return "favorite", tweet.favorite_count

