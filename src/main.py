#!/usr/bin/env python
# coding: utf-8

from classifiers import naive_bayes as nb
from classifiers import svm
from classifiers import maxent as me
from classifiers import decision_tree as dt
from classifiers import majority_vote as mj

from features import fake_feature

import utils as u
import math
import random
# import sys

devset = u.json_to_tweets('../data/dataset.json', True)

# print('# of elements :')
# print(len(devset))

#for elmt in devset:
#    print(str(elmt).encode('ascii', 'xmlcharrefreplace'))
# sys.exit()

retweet = u.tag_as_retweet(devset)
print(u.tag_as_retweet(retweet))
print(len(retweet))

size       = int(math.floor(len(devset)*0.6666))
train_data = devset[0:-size]
test_data  = devset[-size+1:]

train_instances = []
train_labels    = []
for elmt in train_data:
    fake = fake_feature.FakeFeature()
    feat,val = fake.extract(elmt)
    train_instances.append({feat: val})
    train_labels.append(str(random.randint(0,1)))

test_instances = []
test_labels    = []
for elmt in train_data:
    fake = fake_feature.FakeFeature()
    feat,val = fake.extract(elmt)
    test_instances.append({feat: val})
    test_labels.append(str(random.randint(0,1)))

classifier = nb.NaiveBayes()
classifier.train(train_labels, train_instances)
accuracy,_ = classifier.test(test_labels, test_instances)
print('Accuracy NB: %.2f%%\n') % (accuracy)

classifier2 = svm.SVM()
classifier2.train(train_labels, train_instances)
accuracy2,_ = classifier2.test(test_labels, test_instances)
print('Accuracy SVM: %.2f%%\n') % (accuracy2)

classifier3 = me.MaxEnt()
classifier3.train(train_labels, train_instances)
accuracy3,_ = classifier3.test(test_labels, test_instances)
print('Accuracy MaxEnt: %.2f%%\n') % (accuracy3)

classifier4 = dt.DecisionTree()
classifier4.train(train_labels, train_instances)
accuracy4,_ = classifier4.test(test_labels, test_instances)
print('Accuracy Decision Tree: %.2f%%\n') % (accuracy4)

classifier5 = dt.DecisionTree()
classifier5.train(train_labels, train_instances)
accuracy5,_ = classifier5.test(test_labels, test_instances)
print('Accuracy Majority: %.2f%%\n') % (accuracy5)

