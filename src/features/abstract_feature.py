class AbstractFeature:

    def __repr__(self):
        raise NotImplementedError("Please Implement this method")

    def __str__(self):
        raise NotImplementedError("Please Implement this method")

    def extract(self, tweet):
        """Extract the features and return 2 values: key, aka the feature name
        and value aka the extracted feature value."""
        raise NotImplementedError("Please Implement this method")
