from features import abstract_feature as af
import words_processing as wp
import nltk

class TfIdf(af.AbstractFeature):

    def __repr__(self):
        return "<TfIdf>"

    def __str__(self):
        return "TF-IDF"

    def extract(self, tweet):
        freq_max = 0
        text = wp.preprocessing(tweet.text)
        tokens = nltk.word_tokenize(text)

        for word in tokens:
            v = self.data[word]
            if v > freq_max:
                freq_max = v

        return "tf_idf",freq_max
