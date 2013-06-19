# coding: utf-8

class Entities:
    """Represents Twitter entities. Media object has been ommited here."""

    def __init__(self, hashtags, urls, user_mentions):
        """
        hashtags is an array of hashtags object
        urls is an array of url object
        user_mentions is an array of usermention object
        """
        self.hashtags = hashtags
        self.urls = urls
        self.user_mentions = user_mentions

    def __repr__(self):
        return ("<Entities:"
                "hashtags=%s>") % (self.hashtags)

    def __str__(self):
        user_mentions = [str(mention) for mention in self.user_mentions]
        hashtags      = [str(hashtag) for hashtag in self.hashtags]
        urls          = [str(url) for url in self.urls]

        return ("Entities:\n"
                "hashtags: %s\n"
                "urls: %s\n"
                "user mentions: %s\n") % (','.join(user_mentions),
                                          ','.join(hashtags),
                                          ','.join(urls))
