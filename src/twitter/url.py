# coding: utf-8

class Url:
    """
    Represents Twitter url. indices, expanded_url and url have been ommited as
    we just do not care about them.
    """

    def __init__(self, display_url):
        self.display_url = display_url

    def __repr__(self):
        return ("<Url:"
                "display_url=%s>") % (self.display_url)

    def __str__(self):
        return ("Url: %s\n") % (self.display_url)

