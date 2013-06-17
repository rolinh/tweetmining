from abs import ABCMeta, abstractmethod

class AbstractFeature(metaclass=ABCMeta):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def extract(self, tweet):
        """Extract the features and return 2 values: key, aka the feature name
        and value aka the extracted feature value."""
        pass

