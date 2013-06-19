# coding: utf-8

class Hashtags:
    """
    Represents Twitter hashtags. indices has been ommited as we just do not
    care about it.
    """

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return ("<Hashtags:"
                "text=%s>") % (self.text)

    def __str__(self):
        return ("Hashtag value:\n"
                "text: %s\n") % (self.text)

