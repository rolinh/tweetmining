from classifiers import abstract_classifier as ac
from classifiers import classifiers_helper as helper
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

        if self.plot_roc:

            feat_list = test_set[0].keys()
            # FIXME: handle output file name
            outfile = '../data/dt.dot'
            print("ROC curve unavailable for this classifier.\n" +
                  "Creating a Decision Tree plot instead in: %s") % (outfile)
            tree.export_graphviz(self.classifier, outfile, feat_list)

        return helper.accuracy(labels, predictions), predictions
