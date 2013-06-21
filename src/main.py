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
from features import tweet_length_feature
from features import hashtag_count_feature
from features import user_mentions_count_feature
from features import favorite_feature

import utils as u
import math
import random
import sys

devset = u.json_to_tweets('../data/dataset.json', False)

# print('# of elements :')
# print(len(devset))

#retweet = u.tag_as_retweet(devset)
#print(u.tag_as_retweet(retweet))
#print(len(retweet))

#random.shuffle(devset)

size       = int(math.floor(len(devset)*0.6666))
train_data = devset[0:-size]
test_data  = devset[-size+1:]

feat_objs    = [followers_feature.FollowersFeature(),
                statuses_feature.StatusesFeature(),
                tweet_length_feature.TweetLengthFeature(),
                hashtag_count_feature.HashtagCountFeature(),
                user_mentions_count_feature.UserMentionsCountFeature(),
                favorite_feature.FavoriteFeature()]
classif_objs = [nb.NaiveBayes(),
                svm.SVM(),
                #me.MaxEnt(),
                dt.DecisionTree(),
                mv.MajorityVote()]

# extracting training instances
train_instances = []
train_labels    = []
for elmt in train_data:
    features = {}

    for f in feat_objs:
        feat,val = f.extract(elmt)
        features[feat] = val

    train_instances.append(features)
    train_labels.append(u.bool_as_label(elmt.retweet_count > 0))

# extracting test instances
test_instances = []
test_labels    = []
for elmt in train_data:
    features = {}

    for f in feat_objs:
        feat,val = f.extract(elmt)
        features[feat] = val

    test_instances.append(features)
    test_labels.append(u.bool_as_label(elmt.retweet_count > 0))

# classification
for c in classif_objs:
    c.train(train_labels, train_instances)
    accuracy,_ = c.test(test_labels, test_instances)
    print('Accuracy %s: %.2f%%\n') % (str(c), accuracy)
