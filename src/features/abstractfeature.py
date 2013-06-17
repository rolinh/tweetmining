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
        pass

