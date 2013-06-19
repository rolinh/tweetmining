#!/usr/bin/env python
# coding: utf-8

import utils as u

devset = u.json_to_tweets('../data/foo.json')

print('# of elements :')
print(len(devset))

for elmt in devset:
    print(elmt)
