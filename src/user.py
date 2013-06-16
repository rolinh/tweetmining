class User:
    """Represents a Twitter user"""

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return ("<User:"
                "id=%s>") % (self.id)

    def __str__(self):
        return ("User attributes:\n"
                "id: %s\n") % (self.id)

