import user as u

class Tweet:
    """Represents a tweet"""

    def __init__(self,
                 id,
                 user_id,
                 created_at,
                 text,
                 in_reply_to_status_id,
                 in_reply_to_user_id):
        self.id = id
        self.user = u.User(user_id)
        self.created_at = created_at
        self.text = text
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id

    def __repr__(self):
        return ("<Tweet:"
                "id=%s,"
                "user=%s,"
                "created_at=%s,"
                "text=%s,"
                "in_reply_to_status_id=%s,"
                "in_reply_to_user_id=%s>") % (self.id,
                                              str(self.user),
                                              self.created_at,
                                              self.text,
                                              self.in_reply_to_status_id,
                                              self.in_reply_to_user_id)

    def __str__(self):
        return ("Tweet attributes:\n"
                "id: %s\n"
                "user: %s\n"
                "created_at: %s\n"
                "text: %s\n"
                "in_reply_to_status_id: %s\n"
                "in_reply_to_user_id: %s\n") % (self.id,
                                                str(self.user),
                                                self.created_at,
                                                self.text,
                                                self.in_reply_to_status_id,
                                                self.in_reply_to_user_id)
