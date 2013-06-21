# coding: utf-8

class User:
    """Represents a Twitter user"""

    def __init__(self,
                 id,
                 screen_name,
                 favourites_count,
                 followers_count,
                 friends_count,
                 statuses_count,
                 verified):
        self.id = id
        self.screen_name = screen_name
        self.favourites_count = favourites_count
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
        self.verified = verified

    def __repr__(self):
        return ("<User:"
                "id=%s,"
                "screen_name=%s,"
                "favourites_count=%s,"
                "followers_count=%s,"
                "friends_count=%s,"
                "statuses_count=%s,"
                "verified=%s>") % (self.id,
                                   self.screen_name,
                                   self.favourites_count,
                                   self.followers_count,
                                   self.friends_count,
                                   self.statuses_count,
                                   self.verified)

    def __str__(self):
        return ("User attributes:\n"
                "id: %s\n"
                "screen_name: %s\n"
                "favourites_count: %s\n"
                "followers_count: %s\n"
                "friends_count: %s\n"
                "statuses_count: %s\n"
                "verified: %s\n") % (self.id,
                                     self.screen_name,
                                     self.favourites_count,
                                     self.followers_count,
                                     self.friends_count,
                                     self.statuses_count,
                                     self.verified)
