from classifiers import abstract_svm as asvm

class SVMLinear(asvm.AbstractSVM):

    def __repr__(self):
        return "<SVMLinear>"

    def __str__(self):
        return "Support Vector Machine with linear kernel"

    def train(self, labels, train_set):
        super(SVMLinear, self).train_helper(labels, train_set, 'linear')

