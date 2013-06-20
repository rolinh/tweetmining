# coding: utf-8

class Tweet:
    """Represents a tweet"""

    def __init__(self,
                 id,
                 user,
                 created_at,
                 text,
                 entities,
                 in_reply_to_status_id,
                 in_reply_to_user_id,
                 favorite_count,
                 retweet_count):
        self.id = id
        self.user = user
        self.created_at = created_at
        self.text = text
        self.entities = entities
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count

    def __repr__(self):
        return ("<Tweet:"
                "id=%s,"
                "user=%s,"
                "created_at=%s,"
                "text=%s,"
                "entities=%s,"
                "in_reply_to_status_id=%s,"
                "in_reply_to_user_id=%s,"
                "favorite_count=%s,"
                "retweet_count=%s>") % (self.id,
                                        self.user,
                                        self.created_at,
                                        self.text,
                                        self.entities,
                                        self.in_reply_to_status_id,
                                        self.in_reply_to_user_id,
                                        self.favorite_count,
                                        self.retweet_count)

    def __str__(self):
        return ("Tweet attributes:\n"
                "id: %s\n"
                "user: %s\n"
                "created_at: %s\n"
                "text: %s\n"
                "entities: %s\n"
                "in_reply_to_status_id: %s\n"
                "in_reply_to_user_id: %s\n"
                "favorite_count: %s\n"
                "retweet_count: %s\n") % (self.id,
                                          str(self.user),
                                          self.created_at,
                                          self.text,
                                          self.entities,
                                          self.in_reply_to_status_id,
                                          self.in_reply_to_user_id,
                                          self.favorite_count,
                                          self.retweet_count)

