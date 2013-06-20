from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
from nltk.classify import decisiontree

class DecisionTree(ac.AbstractClassifier):

    def train(self, labels, train_set):
        data = helper.format_for_nltk(labels, train_set)
        self.classifier = decisiontree.DecisionTreeClassifier.train(data)

    def test(self, labels, test_set):
        if self.classifier == None:
            return []

        predictions = [self.classifier.classify(inst) for inst in test_set]
        return helper.accuracy(labels, predictions), predictions
