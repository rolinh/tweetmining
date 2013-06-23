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
import argparse

def classification_routine(train_data, test_data, feat_objs, classif_objs):
    """run the classification process with feature extraction stuff and
    prediction. It returns a coningency table and a list of accuracies"""

    # extracting training instances
    print("Extracting training instances...")
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
    print("Extracting test instances...\n")
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

def cross_validation(dataset, feat_objs, classif_objs):
    length     = len(dataset)
    subsize    = int(math.floor(length*0.1))
    maxiter    = int(math.floor(float(length) / float(subsize)))

    print('Length:\t%d')  % (length)
    print('Subsize:\t%d') % (subsize)
    print('Maxiter:\t%d') % (maxiter)

    print('#####################################################')

    for i in range(0,maxiter):
        print('step %d/%d\n') % (i+1, maxiter)

        start = i * subsize
        end   = start + subsize-1

        test_data = dataset[start:end+1]

        # handle test data position
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
        print('accuracy -> ')
        for i,v in enumerate(acc):
            print('\t%s: %.2f%%') % (classif_objs[i], v)
        print('#####################################################')

def main(classification=True,
         tournament=False,
         x_validation=False,
         devset=False,
         randomize=False,
         verbose=False):
    """main function"""

    if devset:
        print("Using development dataset")
        set_file = '../data/devset.json'
        wocc_file = '../data/devset_words_occurrence.txt'
    else:
        print("Using full dataset")
        set_file = '../data/dataset.json'
        wocc_file = '../data/dataset_words_occurrence.txt'

    print("Collecting data...")
    dataset = u.json_to_tweets(set_file, False)
    print("Loading words occurrencies...")
    words_occ = u.words_occ_to_dict(wocc_file)
    print("Computing term frequency...")
    words_tf = u.words_occ_to_tf(words_occ)
    print("Computing term frequency - inverse document frequency...")
    words_tf_idf = u.words_occ_to_tfidf(words_occ)

    if randomize:
        print("Randomizing dataset...")
        random.shuffle(dataset)

    feat_objs    = [followers_count_feature.FollowersCountFeature(),
                    statuses_count_feature.StatusesCountFeature(),
                    tweet_length_feature.TweetLengthFeature(),
                    hashtag_count_feature.HashtagCountFeature(),
                    # hashtag_popularity_feature.HashtagPopularityFeature(),
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
    if verbose:
        print("\nFeatures activated:")
        for feat in feat_objs:
            print("- %s") % (str(feat))
        print("\nClassifiers used:")
        for cl in classif_objs:
            print("- %s") % (str(cl))
        print("")

    size       = int(math.floor(len(dataset)*0.6666))
    train_data = dataset[0:-size]
    test_data  = dataset[-size+1:]

    if classification:
        print("Starting classification...")
        classification_routine(train_data, test_data, feat_objs, classif_objs)

    if x_validation:
        print("Performing cross validation...")
        cross_validation(dataset, feat_objs, classif_objs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='TweetMining',
        description='Predict if a tweet will be retweeted or not.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--all',
                        action='store_true',
                        default=False,
                        help='do all (classification, tournament and \
                        cross-validation')
    parser.add_argument('-c', '--classification',
                        action='store_true',
                        default=False,
                        help='perform classification')
    parser.add_argument('-d', '--dataset',
                        action='store',
                        default='dataset',
                        choices=['devset', 'dataset'],
                        help='dataset to use')
    parser.add_argument('-r', '--randomize',
                        action='store_true',
                        default=False,
                        help='randomize dataset')
    parser.add_argument('-t', '--tournament',
                        action='store_true',
                        default=False,
                        help='perform algorithm tournament')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='increase verbosity')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-x', '--x-validation',
                        action='store_true',
                        default=False,
                        help='perform cross-validation')

    args = parser.parse_args()

    if args.dataset == 'devset':
        dev = True
    else:
        dev = False

    if not (args.all or
            args.classification or
            args.tournament or
            args.x_validation):
        print("No option chosen. Thus simply performing classification.")
        main(True,
             args.tournament,
             args.x_validation,
             dev,
             args.randomize,
             args.verbose)
    elif args.all:
        main(True,
             True,
             True,
             dev,
             args.randomize,
             args.verbose)
    else:
        main(args.classification,
             args.tournament,
             args.x_validation,
             dev,
             args.randomize,
             args.verbose)

    sys.exit(0)
