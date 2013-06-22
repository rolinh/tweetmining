#!/usr/bin/env python
# coding: utf-8

import credentials as c

import json
import codecs
import sys

from twython import Twython, TwythonError

################################################################################
# Configure values below to your needs
search_tag='shampoo'
language='en'
dataset='../data/dataset.json'
################################################################################

min_id = 1000000000000000000000000000000000000000000000000000000000000000000000

# Twitter API >= v1.1 requires an authentification... even to fetch public data!
twitter = Twython(c.APP_CONSUMER_KEY,
                  c.APP_CONSUMER_SECRET,
                  c.OAUTH_TOKEN,
                  c.OAUTH_TOKEN_SECRET)

fp = codecs.open(dataset, 'a', 'utf-8')
for i in range(180):
    try:
        result = twitter.search(q=search_tag,
                                count=100,
                                lang=language,
                                max_id=min_id)
    except TwythonError as e:
        print(e)
        sys.exit(1)

    for tw in result['statuses']:
            id = tw['id']
            if id < min_id:
                min_id = id

    fp.write('\n')
    json.dump(result, fp)

fp.close()
sys.exit(0)
