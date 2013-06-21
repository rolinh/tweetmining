from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
from nltk.classify import naivebayes as nb

class NaiveBayes(ac.AbstractClassifier):

    def __repr__(self):
        return "<NaiveBayes>"

    def __str__(self):
        return "Naive Bayes"

    def train(self, labels, train_set):
        data = helper.format_for_nltk(labels, train_set)
        self.classifier = nb.NaiveBayesClassifier.train(data)

        # TODO use this in the main.py
        self.classifier.show_most_informative_features(5)

    def test(self, labels, test_set):
        if self.classifier == None:
            return []

        predictions = [self.classifier.classify(inst) for inst in test_set]
        return helper.accuracy(labels, predictions), predictions
