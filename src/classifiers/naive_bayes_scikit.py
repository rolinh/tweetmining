from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
#from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB

class NaiveBayesScikit(ac.AbstractClassifier):

    def __repr__(self):
        return "<NaiveBayesScikit>"

    def __str__(self):
        return "Naive Bayes Scikit"

    def train(self, labels, train_set):
        self.classifier = BernoulliNB()
        l,ts = helper.format_for_scikit(labels, train_set)
        self.classifier.fit(ts, l)

    def test(self, labels, test_set):
        l,ts = helper.format_for_scikit(labels, test_set)
        predictions = self.classifier.predict(ts)

        if self.plot_roc:
            print("ROC curve plot unavailable for %s") % (str(self))

        return helper.accuracy(labels, predictions), predictions
