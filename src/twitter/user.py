# coding: utf-8

class User:
    """Represents a Twitter user"""

    def __init__(self, id, screen_name):
        self.id = id
        self.screen_name = screen_name

    def __repr__(self):
        return ("<User:"
                "id=%s,"
                "screen_name=%s>") % (self.id, self.screen_name)

    def __str__(self):
        return ("User attributes:\n"
                "id: %s\n"
                "screen_name: %s\n") % (self.id, self.screen_name)
