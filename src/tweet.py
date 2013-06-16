import user

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
        self.user = User(user_id)
        self.created_at = created_at
        self.text = text
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id

