from classifiers import abstract_svm as asvm

class SVMSigmoid(asvm.AbstractSVM):

    def __repr__(self):
        return "<SVMSigmoid>"

    def __str__(self):
        return "Support Vector Machine with sigmoid kernel"

    def train(self, labels, train_set):
        super(SVMRBF, self).train_helper(labels, train_set, 'sigmoid')

