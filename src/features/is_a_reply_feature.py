from features import abstract_feature as af

class IsAReplyFeature(af.AbstractFeature):

    def __repr__(self):
        return "<IsAReplyFeature>"

    def __str__(self):
        return "Is A Reply Feature"

    def extract(self, tweet):
        is_a_reply = False

        if tweet.in_reply_to_user_id != None:
            is_a_reply = True

        return "is_a_reply", is_a_reply
