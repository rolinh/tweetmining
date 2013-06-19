# coding: utf-8

class UserMention:
    """
    Represents Twitter user_mention. indices and id_str have been ommited as we
    just do not care about them.
    """

    def __init__(self, id, name, screen_name):
        self.id = id
        self.name = name
        self.screen_name = screen_name

    def __repr__(self):
        return ("<UserMention:"
                "id=%s,"
                "name=%s,"
                "screen_name=%s>") % (self.id,
                                      self.name,
                                      self.screen_name)

    def __str__(self):
        return ("User Mention:\n"
                "id: %s\n"
                "name: %s\n"
                "screen name: %s\n") % (self.id,
                                        self.name,
                                        self.screen_name)

