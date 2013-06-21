from features import abstract_feature as af

class VerifiedAccountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<VerifiedAccountFeature>"

    def __str__(self):
        return "Verified Account Feature"

    def extract(self, tweet):
        return "verified_account", tweet.user.verified
