from sklearn import feature_selection as fs
from classifiers import classifiers_helper as helper

class FeaturesSelection:
    """Provides static methods for features selection"""

    @staticmethod
    def chi2(data, labels, print_results=True):
        """Compute chi-squared statistic for each class/feature combination.
        The results are printed (if the `print_results` paramter is True) in
        the stdout AND returned."""

        y, X       = helper.format_for_scikit(labels, data)
        chi2, pval = fs.chi2(X,y)

        feature_names = [name for name in data[0].keys()]

        if print_results:
            print('Chi-squared values for each feature :')
            for i,v in enumerate(chi2):
                print('%s => %f') % (feature_names[i], v)
            print('#####################################')
            print('p-value for each feature :')
            for i,v in enumerate(pval):
                print('%s => %f') % (feature_names[i], v)

        return chi2, pval
