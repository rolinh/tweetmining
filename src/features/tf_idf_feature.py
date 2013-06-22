from features import abstract_feature as af
import features_helper as fh

class TfIdf(af.AbstractFeature):

    def __repr__(self):
        return "<TfIdf>"

    def __str__(self):
        return "TF-IDF"

    def extract(self, tweet):
        return "tf_idf",fh.tf_freq_max(tweet, self.data)
