from abs import ABCMeta, abstractmethod

class AbstractClassifier(metaclass=ABCMeta):
    """Abstract class wrapper for a classifier."""

    classifier = None
    """Trained classifier instance."""

    @abstractmethod
    def train(self, trainset):
        """
        Train a classifier with the given train set.
        `trainset` is expected to be a list of dictionnary where each
        dictionnary represents an instance.
        Example:
        trainset = [{'label':'1', 'feature1':'value1', 'feature2':'value2',...},
                    {'label':'2', 'feature1':'value1', ...}, ...]
        """
        pass

    @abstractmethod
    def test(self, testset):
        """
        Test a classifier with the given test set.
        `testset` is expected to be a list of dictionnary where each
        dictionnary represents an instance.
        Example:
        testset = [{'label':'1', 'feature1':'value1', 'feature2':'value2', ...},
                   {'label':'2', 'feature1':'value1', ...}, ...]
        Return a pair of values: the first one is the accuracy of the classifier
        and the second one is the list of predicted labels.
        """
        pass

