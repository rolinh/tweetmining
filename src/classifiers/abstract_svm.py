from abc import ABCMeta, abstractmethod

from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper

from sklearn import svm

class AbstractSVM(ac.AbstractClassifier):
    """Abstract class wrapper to use different kernels in SVM child classes."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def train(self, labels, train_set):
        pass

    def train_helper(self, labels, train_set, kernel_name, deg=3):
        self.classifier = svm.SVC(kernel=kernel_name, degree=deg,
                                  probability=True)
        l,ts = helper.format_for_scikit(labels, train_set)
        self.classifier.fit(ts, l)

    def test(self, labels, test_set):
        l,ts = helper.format_for_scikit(labels, test_set)
        predictions = self.classifier.predict(ts)

        if self.plot_roc:
            probas = self.classifier.predict_proba(ts)
            helper.roc(probas, l, str(self))

        return helper.accuracy(labels, predictions), predictions

