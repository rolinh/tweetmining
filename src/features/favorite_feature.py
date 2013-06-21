from features import abstract_feature as af

class FavoriteFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FavoriteFeature>"

    def __str__(self):
        return "Favorite Feature"

    def extract(self, tweet):
        return "favorite", tweet.favorite_count

