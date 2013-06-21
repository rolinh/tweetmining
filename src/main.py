#!/usr/bin/env python
# coding: utf-8

from classifiers import naive_bayes as nb
from classifiers import svm
from classifiers import maxent as me
from classifiers import decision_tree as dt
from classifiers import majority_vote as mv

from features import fake_feature
from features import followers_feature
from features import statuses_feature

import utils as u
import math
import random
import sys

devset = u.json_to_tweets('../data/dataset.json', False)

# print('# of elements :')
# print(len(devset))

#for elmt in devset:
#    print(str(elmt).encode('ascii', 'xmlcharrefreplace'))
# sys.exit()

#retweet = u.tag_as_retweet(devset)
#print(u.tag_as_retweet(retweet))
#print(len(retweet))

random.shuffle(devset)

size       = int(math.floor(len(devset)*0.6666))
train_data = devset[0:-size]
test_data  = devset[-size+1:]

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

"""for elmt in test_data:
    try:
        print(str(elmt))
    except UnicodeEncodeError:
        pass
sys.exit()"""

train_instances = []
train_labels    = []
for elmt in train_data:
    features = {}

    followers = followers_feature.FollowersFeature()
    feat,val = followers.extract(elmt)
    features[feat] = val

    statuses = statuses_feature.StatusesFeature()
    feat,val = statuses.extract(elmt)
    features[feat] = val

    train_instances.append(features)

    train_labels.append(u.bool_as_label(elmt.retweet_count > 0))

test_instances = []
test_labels    = []
for elmt in train_data:
    features = {}

    followers = followers_feature.FollowersFeature()
    feat,val = followers.extract(elmt)
    features[feat] = val

    statuses = statuses_feature.StatusesFeature()
    feat,val = statuses.extract(elmt)
    features[feat] = val

    test_instances.append(features)

    test_labels.append(u.bool_as_label(elmt.retweet_count > 0))

classifier = nb.NaiveBayes()
classifier.train(train_labels, train_instances)
accuracy,_ = classifier.test(test_labels, test_instances)
print('Accuracy Naive Bayes: %.2f%%\n') % (accuracy)

classifier2 = svm.SVM()
classifier2.train(train_labels, train_instances)
accuracy2,_ = classifier2.test(test_labels, test_instances)
print('Accuracy Support Vector Machine: %.2f%%\n') % (accuracy2)

classifier3 = me.MaxEnt()
classifier3.train(train_labels, train_instances)
accuracy3,_ = classifier3.test(test_labels, test_instances)
print('Accuracy Maximum Entropy: %.2f%%\n') % (accuracy3)

classifier4 = dt.DecisionTree()
classifier4.train(train_labels, train_instances)
accuracy4,_ = classifier4.test(test_labels, test_instances)
print('Accuracy Decision Tree: %.2f%%\n') % (accuracy4)

classifier5 = mv.MajorityVote()
classifier5.train(train_labels, train_instances)
accuracy5,_ = classifier5.test(test_labels, test_instances)
print('Accuracy Majority Vote: %.2f%%\n') % (accuracy5)
