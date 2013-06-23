#!/usr/bin/env python
# coding: utf-8

from classifiers import naive_bayes as nb
from classifiers import naive_bayes_scikit as nbs
from classifiers import svm_rbf
from classifiers import svm_sigmoid
from classifiers import svm_poly
from classifiers import svm_linear
from classifiers import maxent as me
from classifiers import maxent_scikit as mes
from classifiers import lda
from classifiers import decision_tree as dt
from classifiers import decision_tree_scikit as dts
from classifiers import majority_vote as mv

from features import fake_feature
from features import followers_count_feature
from features import statuses_count_feature
from features import tweet_length_feature
from features import hashtag_count_feature
from features import user_mentions_count_feature
from features import favorite_count_feature
from features import has_url_feature
from features import friends_count_feature
from features import verified_account_feature
from features import tf_feature
from features import tf_idf_feature

import utils as u
import words_processing as wp

import math
import random
import sys

def extract_train_instances(dataset, feat_objs):
    """Extract instances from the data set and returns the instances as an
    array of dictionary and the list of labels"""

    # extracting features from data set
    print("Extracting features from data set...")
    instances = []
    labels    = []
    for elmt in dataset:
        features = {}

        for f in feat_objs:
            feat,val = f.extract(elmt)
            features[feat] = val

        instances.append(features)
        labels.append(u.bool_as_label(elmt.retweet_count > 0))

    return instances, labels

def classification_routine(train_instances, test_instances, classif_objs):
    """Run the classification process with feature extraction stuff and
    prediction. It returns a list of accuracies and a list of lists of
    predictions."""

    # classification
    accuracies_list  = []
    predictions_list = []
    for c in classif_objs:
        print("Classifying using %s...") % str(c)
        c.train(train_labels, train_instances)
        accuracy,predictions = c.test(test_labels, test_instances)
        print('Accuracy %s: %.2f%%\n') % (str(c), accuracy)
        accuracies_list.append(accuracy)
        predictions_list.append(predictions)

    return accuracies_list, predictions_list

def cross_validation(instances, labels, classif_objs):
    dataset    = []
    [dataset.append(v) for v in test_instances]
    [dataset.append(v) for v in train_instances]

    length     = len(dataset)
    subsize    = int(math.floor(length*0.1))
    maxiter    = int(math.floor(float(length) / float(subsize)))

    print('Calculating cross-validation...\n')
    print('Length:\t%d')  % (length)
    print('Subsize:\t%d') % (subsize)
    print('Maxiter:\t%d') % (maxiter)
    print('#####################################################')

    r = range(0, len(classif_objs))
    average_accuracies = [0.0 for i in r]
    all_predictions    = []

    for i in range(0,maxiter):
        print('step %d/%d\n') % (i+1, maxiter)

        start = i * subsize
        end   = start + subsize-1

        test_data = dataset[start:end+1]

        # handle train data position
        if start == 0:
            train_data  = dataset[end+1:]
        elif end == maxiter * subsize:
            # TODO CHECK THIS !
            if maxiter * subsize == length:
                train_data  = dataset[:start-1]
            else:
                train_data = dataset[:start]
                for v in dataset[end+1:]:
                    train_data.append(v)
        else:
            train_data  = dataset[0:start]
            for v in dataset[end+1:]:
                train_data.append(v)

        acc, pred = classification_routine(train_data, test_data,
                                           feat_objs, classif_objs)
        all_predictions.append(pred)

        # update average accuracies
        for i,v in enumerate(acc):
            average_accuracies[i] += v

        print('accuracy -> ')
        for i,v in enumerate(acc):
            print('\t%s: %.2f%%') % (classif_objs[i], v)
        print('#####################################################')

    # average the accuracies
    for i,v in enumerate(average_accuracies):
        average_accuracies[i] = float(v) / float(maxiter)

    return average_accuracies, all_predictions

def algorithm_tournament(instances, labels, feat_objs, classif_objs):
    """Algorithm tournament"""

    acc, pred = cross_validation(dataset, feat_objs, classif_objs)
    indices   = range(0, len(classif_objs))
    scores    = [0 for i in range(0, len(classif_objs))]

    average_acc, all_predic = cross_validation(instances, labels, classif_objs)

    for ind in itertools.combinations(indices, length):
        i1 = ind[0]
        i2 = ind[1]
        c1 = str(classif_objs[i1])
        c2 = str(classif_objs[i2])

        contingency_table  = [[0, 0], [0, 0]]

        for turn in all_predic:
            res1 = turn[i1]
            res2 = turn[i2]

            local_table = [[0, 0], [0, 0]]

            for i in range(0, len(res1)):
                if res1[i] == res2[i] and res1[i] == labels[i]:
                    local_table[1][1] += 1
                elif res1[i] == res2[i] and res1[i] != labels[i]:
                    local_table[0][0] += 1
                elif res1[i] != labels[i]:
                    local_table[0][1] += 1
                else:
                    local_table[1][0] += 1

            # give score
            if local_table[0][1] > local_table[0][1]:
                score[i2] += 1
            elif local_table[0][1] < local_table[0][1]:
                score[i1] += 1
            else:
                score[i1] += 0.5
                score[i2] += 0.5

            # update contingency table
            contingency_table[0][0] += local_table[0][0]
            contingency_table[0][1] += local_table[0][1]
            contingency_table[1][0] += local_table[1][0]
            contingency_table[1][1] += local_table[1][1]

        # perform mcnemar test
        signi = u.mcnemar(contingency_table)

        winner = 'egality !'
        if contingency_table[0][1] > contingency_table[0][1]
            winner = str(c2)
        elif contingency_table[0][1] < contingency_table[0][1]
            winner = str(c1)
        print('%s vs %s') % (str(c1), str(c2))
        print('The winner is : %s') % (winner)
        print('McNemar test: %s') % (u.mcnemar(contingency_table))
        print('################')

    # tournament results
    print('\nTournament results :')
    for i,v in enumerate(score):
        print('%s: %f') % (classif_objs[i], v)

def main(args):
    """main function"""
    print("Collecting data...")

    dataset = u.json_to_tweets('../data/devset.json', False)
    words_occ = u.words_occ_to_dict('../data/devset_words_occurrence.txt')
    words_tf = u.words_occ_to_tf(words_occ)
    words_tf_idf = u.words_occ_to_tfidf(words_occ)

    #random.shuffle(devset)

    feat_objs    = [followers_count_feature.FollowersCountFeature(),
                    statuses_count_feature.StatusesCountFeature(),
                    tweet_length_feature.TweetLengthFeature(),
                    hashtag_count_feature.HashtagCountFeature(),
                    user_mentions_count_feature.UserMentionsCountFeature(),
                    favorite_count_feature.FavoriteCountFeature(),
                    has_url_feature.HasUrlFeature(),
                    friends_count_feature.FriendsCountFeature(),
                    verified_account_feature.VerifiedAccountFeature(),
                    tf_feature.Tf(data=words_tf),
                    tf_idf_feature.TfIdf(data=words_tf_idf)]
    classif_objs = [nb.NaiveBayes(),
                    nbs.NaiveBayesScikit(),
                    svm_rbf.SVMRBF(),
                    svm_sigmoid.SVMSigmoid(),
                    #svm_poly.SVMPoly(),
                    #svm_linear.SVMLinear(),
                    #me.MaxEnt(),
                    lda.LDA(),
                    mes.MaxEntScikit(),
                    dts.DecisionTreeScikit(),
                    dt.DecisionTree(),
                    mv.MajorityVote()]

    # "normal" classifications
    size       = int(math.floor(len(dataset)*0.6666))
    train_data = dataset[0:-size]
    test_data  = dataset[-size+1:]
    #classification_routine(train_data, test_data, feat_objs, classif_objs)

    # cross validatation
    cross_validation(dataset, feat_objs, classif_objs)

if __name__ == "__main__":
    main(sys.argv)
