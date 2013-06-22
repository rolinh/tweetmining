from features import abstract_feature as af
import words_processing as wp
import nltk

class Tf(af.AbstractFeature):

    def __repr__(self):
        return "<Tf>"

    def __str__(self):
        return "TF"

    def extract(self, tweet):
        freq_max = 0
        text = wp.preprocessing(tweet.text)
        tokens = nltk.word_tokenize(text)

        for word in tokens:
            v = self.data[word]
            if v > freq_max:
                freq_max = v

        return "tf",freq_max
