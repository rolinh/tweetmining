#!/usr/bin/env python
# coding: utf-8

import credentials as c
from twython import Twython, TwythonError

# Twitter API >= v1.1 requires an authentification... even to fetch public data!
twitter = Twython(c.APP_CONSUMER_KEY,
                  c.APP_CONSUMER_SECRET,
                  c.OAUTH_TOKEN,
                  c.OAUTH_TOKEN_SECRET)

try:
    result = twitter.search(q='shampoo', count=100, lang='en')
except TwythonError as e:
    print(e)

f = open('../data/devset.json', 'w')
f.write(str(result))
f.close()
