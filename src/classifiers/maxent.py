from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
from nltk.classify import maxent

class MaxEnt(ac.AbstractClassifier):

    def __repr__(self):
        return "<MaxEnt>"

    def __str__(self):
        return "Maximum Entropy"

    def train(self, labels, train_set):
        data = helper.format_for_nltk(labels, train_set)
        self.classifier = maxent.MaxentClassifier.train(data)

        # TODO use this in the main.py
        self.classifier.show_most_informative_features(5)

    def test(self, labels, test_set):
        if self.classifier == None:
            return []

        predictions = [self.classifier.classify(inst) for inst in test_set]

        if self.plot_roc:
            print("ROC curve plot unavailable for %s") % (str(self))

        return helper.accuracy(labels, predictions), predictions
