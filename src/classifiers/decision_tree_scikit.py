from classifiers import abstract_classifier as ac
from sklearn import tree

class DecisionTreeScikit(ac.AbstractClassifier):

    def __repr__(self):
        return "<DecisionTreeScikit>"

    def __str__(self):
        return "Decision Tree Scikit"

    def train(self, labels, train_set):
        self.classifier = tree.DecisionTreeClassifier()
        l,ts = helper.format_for_scikit(labels, train_set)
        self.classifier.fit(ts, l)

    def test(self, labels, test_set):
        _,ts = helper.format_for_scikit(labels, test_set)
        predictions = self.classifier.predict(ts)
        return helper.accuracy(labels, predictions), predictions
