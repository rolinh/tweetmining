from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper

class MajorityVote(ac.AbstractClassifier):

    def train(self, labels, train_set):
        self.classifier = helper.highest_bin_freq(labels)

    def test(self, labels, test_set):
        if self.classifier == None:
            return []

        predictions = [self.classifier] * len(test_set)
        return helper.accuracy(labels, predictions), predictions
