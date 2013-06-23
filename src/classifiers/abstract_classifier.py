from abc import ABCMeta, abstractmethod

class AbstractClassifier:
    """Abstract class wrapper for a classifier."""
    __metaclass__ = ABCMeta

    classifier = None
    """Trained classifier instance."""

    def __init__(self, plot_roc=False):
        self.plot_roc = plot_roc

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def train(self, labels, train_set):
        """
        Train a classifier with the given train set.
        `labels` must be a list that contains the class for each instance of
        the training set and `trainset` is expected to be a list of dictionnary
        where each dictionnary represents an instance.
        Example:
        trainset = [{'feature1':'value1', 'feature2':'value2',...},
                    {'feature1':'value1', ...}, ...]
        """
        pass

    @abstractmethod
    def test(self, labels, test_set):
        """
        Test a classifier with the given test set.
        `labels` must be a list that contains the class for each instance of

        the test set and `testset` is expected to be a list of dictionnary where
        each dictionnary represents an instance.
        Example:
        testset = [{'feature1':'value1', 'feature2':'value2', ...},
                   {'feature1':'value1', ...}, ...]
        Return a pair of values: the first one is the accuracy of the classifier
        and the second one is the list of predicted labels.
        """
        pass
