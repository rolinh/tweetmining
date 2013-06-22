from features import abstract_feature as af
import features_helper as fh

class Tf(af.AbstractFeature):

    def __repr__(self):
        return "<Tf>"

    def __str__(self):
        return "TF"

    def extract(self, tweet):
        return "tf",fh.tf_freq_max(tweet, self.data)
