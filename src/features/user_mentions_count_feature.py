from features import abstract_feature as af

class UserMentionsCountFeature(af.AbstractFeature):

    def __repr__(self):
        return "<UserMentionsCountFeature>"

    def __str__(self):
        return "User Mentions Count Feature"

    def extract(self, tweet):
        return "user_mentions_count", len(tweet.entities.user_mentions)
