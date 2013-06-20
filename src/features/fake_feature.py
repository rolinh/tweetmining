from features import abstract_feature as af

class FakeFeature(af.AbstractFeature):

    def __repr__(self):
        return "<FakeFeature>"

    def __str__(self):
        return "Fake Feature"

    def extract(self, tweet):
        return "fake", "42"

