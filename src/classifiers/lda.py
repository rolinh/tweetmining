from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
from sklearn import lda

class LDA(ac.AbstractClassifier):

    def __repr__(self):
        return "<LDAScikit>"

    def __str__(self):
        return "Linear Discriminant Analysis Scikit"

    def train(self, labels, train_set):
        self.classifier = lda.LDA()
        l,ts = helper.format_for_scikit(labels, train_set)
        self.classifier.fit(ts, l)

    def test(self, labels, test_set):
        _,ts = helper.format_for_scikit(labels, test_set)
        predictions = self.classifier.predict(ts)
        return helper.accuracy(labels, predictions), predictions
