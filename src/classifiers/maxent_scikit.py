from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
from sklearn import linear_model

class MaxEntScikit(ac.AbstractClassifier):

    def __repr__(self):
        return "<MaxEntscikit>"

    def __str__(self):
        return "Maximum Entropy Scikit"

    def train(self, labels, train_set):
        self.classifier = linear_model.LogisticRegression()
        l,ts = helper.format_for_scikit(labels, train_set)
        self.classifier.fit(ts, l)

    def test(self, labels, test_set):
        _,ts = helper.format_for_scikit(labels, test_set)
        predictions = self.classifier.predict(ts)

        if self.plot_roc:
            print("ROC curve plot unavailable for %s") % (str(self))

        return helper.accuracy(labels, predictions), predictions
