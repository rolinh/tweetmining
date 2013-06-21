from features import abstract_feature as af

class FavoriteCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FavoriteCountFeature>"

    def __str__(self):
        return "Favorite Count Feature"

    def extract(self, tweet):
        return "favorite_count", tweet.favorite_count

