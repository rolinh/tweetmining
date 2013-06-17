from features import abstract_feature

class FakeFeature(AbstractFeature):

    def __repr__(self):
        return "<FakeFeature>"

    def __str__(self):
        return "Fake Feature"

    def extract(self, tweet):
        return "fake", "42"

