from classifiers import abstract_svm as asvm

class SVMPoly(asvm.AbstractSVM):

    def __repr__(self):
        return "<SVMPoly>"

    def __str__(self):
        return "Support Vector Machine with polynomial kernel"

    def train(self, labels, train_set):
        super(SVMRBF, self).train_helper(labels, train_set, 'poly')

