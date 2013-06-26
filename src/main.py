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
from classifiers import features_selection as fs

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
from features import is_a_retweet_feature
from features import tweet_age_feature
from features import is_a_reply_feature

import utils as u
import words_processing as wp

from sklearn import metrics
from multiprocessing import Process

import math
import random
import sys
import argparse
import itertools

def extract_instances(dataset, feat_objs):
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

def classification_routine(train_inst, test_inst, train_labels,
                           test_labels, classif_objs):
    """Run the classification process with feature extraction stuff and
    prediction. It returns a list of accuracies and a list of lists of
    predictions."""

    print("Starting classification...")

    # classification
    accuracies_list  = []
    predictions_list = []
    for c in classif_objs:
        print("Classifying using %s...") % str(c)
        c.train(train_labels, train_inst)
        accuracy,predictions = c.test(test_labels, test_inst)
        print('Accuracy %s: %.2f%%\n') % (str(c), accuracy)
        accuracies_list.append(accuracy)
        predictions_list.append(predictions)

    return accuracies_list, predictions_list

def cross_validation(instances, labels, classif_objs):
    length     = len(instances)
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
    all_labels         = []

    for i in range(0,maxiter):
        print('step %d/%d\n') % (i+1, maxiter)

        start = i * subsize
        end   = start + subsize-1

        test_data   = instances[start:end+1]
        test_labels = labels[start:end+1]

        # handle train data position
        if start == 0:
            train_data   = instances[end+1:]
            train_labels = labels[end+1:]
        elif end == maxiter * subsize:
            # TODO CHECK THIS !
            if maxiter * subsize == length:
                train_data   = instances[:start-1]
                train_labels = labels[:start-1]
            else:
                train_data   = instances[:start]
                train_labels = labels[:start]

                for v in instances[end+1:]:
                    train_data.append(v)

                for v in labels[end+1:]:
                    train_labels.append(v)
        else:
            train_data   = instances[0:start]
            train_labels = labels[0:start]

            for v in instances[end+1:]:
                train_data.append(v)

            for v in labels[end+1:]:
                train_labels.append(v)

        acc, pred = classification_routine(train_data, test_data, train_labels,
                                           test_labels, classif_objs)
        all_predictions.append(pred)
        all_labels.append(test_labels)

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

    return average_accuracies, all_predictions, all_labels

def algorithm_tournament(instances, full_labels, classif_objs):
    """Algorithm tournament"""

    indices   = range(0, len(classif_objs))
    scores    = [0 for i in range(0, len(classif_objs))]

    average_acc, all_predic, labels = cross_validation(instances, full_labels, classif_objs)

    for ind in itertools.combinations(indices, 2):
        i1 = ind[0]
        i2 = ind[1]
        c1 = str(classif_objs[i1])
        c2 = str(classif_objs[i2])

        contingency_table  = [[0, 0], [0, 0]]

        for turn_ind, turn in enumerate(all_predic):
            res1 = turn[i1]
            res2 = turn[i2]

            local_table = [[0, 0], [0, 0]]

            for i in range(0, len(res1)):
                if str(res1[i]) == labels[turn_ind][i] and str(res2[i]) == labels[turn_ind][i]:
                    local_table[1][1] += 1
                elif str(res1[i]) != labels[turn_ind][i] and str(res2[i]) != labels[turn_ind][i]:
                    local_table[0][0] += 1
                elif str(res1[i]) != labels[turn_ind][i] and str(res2[i]) == labels[turn_ind][i]:
                    local_table[0][1] += 1
                else:
                    local_table[1][0] += 1

            # give score
            if local_table[0][1] > local_table[1][0]:
                scores[i2] += 1
            elif local_table[0][1] < local_table[1][0]:
                scores[i1] += 1
            else:
                scores[i1] += 0.5
                scores[i2] += 0.5

            # print('local table :')
            # print(local_table)
            # update contingency table
            contingency_table[0][0] += local_table[0][0]
            contingency_table[0][1] += local_table[0][1]
            contingency_table[1][0] += local_table[1][0]
            contingency_table[1][1] += local_table[1][1]

        # perform mcnemar test
        signi = u.mcnemar(contingency_table)

        print('Contingency table :')
        print(contingency_table)

        winner = 'tie !'
        if contingency_table[0][1] > contingency_table[1][0]:
            winner = c2
        elif contingency_table[0][1] < contingency_table[1][0]:
            winner = c1
        print('%s vs %s') % (c1, c2)
        print('The winner is : %s') % (winner)
        print('McNemar test: %s') % (str(u.mcnemar(contingency_table)))
        print('################')

    # tournament results
    print('\nTournament results :')
    for i,v in enumerate(scores):
        print('%s: %.1f') % (classif_objs[i], v)

def main(classification=True,
         tournament=False,
         x_validation=False,
         devset=False,
         randomize=False,
         verbose=False,
         plot_roc=False,
         multiprocessing=False):
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

    if verbose:
        f = "%Y-%m-%d"
        oldest_tweet, newest_tweet = u.tweets_date_range(dataset)
        print("Oldest tweet was posted on %s") % (oldest_tweet).strftime(f)
        print("Newest tweet was posted on %s") % (newest_tweet).strftime(f)
        print("Date range is %d day(s)") % (newest_tweet - oldest_tweet).days

    print("Loading words occurrencies...")
    words_occ = u.words_occ_to_dict(wocc_file)
    print("Computing term frequency...")
    words_tf = u.words_occ_to_tf(words_occ)
    print("Computing term frequency - inverse document frequency...")
    words_tf_idf = u.words_occ_to_tfidf(words_occ)

    if randomize:
        print("Randomizing dataset...")
        random.shuffle(dataset)

    # list of objects containing the feature classes
    feat_objs    = [
                    #fake_feature.FakeFeature(),
                    is_a_retweet_feature.IsARetweetFeature(),
                    is_a_reply_feature.IsAReplyFeature(),
                    followers_count_feature.FollowersCountFeature(),
                    #tweet_age_feature.TweetAgeFeature(),
                    tweet_length_feature.TweetLengthFeature(),
                    statuses_count_feature.StatusesCountFeature(),
                    hashtag_count_feature.HashtagCountFeature(),
                    user_mentions_count_feature.UserMentionsCountFeature(),
                    favorite_count_feature.FavoriteCountFeature(),
                    has_url_feature.HasUrlFeature(),
                    friends_count_feature.FriendsCountFeature(),
                    #verified_account_feature.VerifiedAccountFeature(),
                    #tf_feature.Tf(data=words_tf),
                    #tf_idf_feature.TfIdf(data=words_tf_idf)
                    ]

    # list of objects containing the classifier classes
    classif_objs = [
                    #nb.NaiveBayes(plot_roc),
                    nbs.NaiveBayesScikit(plot_roc),
                    svm_rbf.SVMRBF(plot_roc),
                    svm_sigmoid.SVMSigmoid(plot_roc),
                    #svm_poly.SVMPoly(plot_roc),
                    #svm_linear.SVMLinear(plot_roc),
                    #me.MaxEnt(plot_roc),
                    mes.MaxEntScikit(plot_roc),
                    dts.DecisionTreeScikit(plot_roc),
                    #dt.DecisionTree(plot_roc),
                    mv.MajorityVote(plot_roc),
                    lda.LDA(plot_roc)
                    ]
    if verbose:
        print("\nFeatures activated:")
        for feat in feat_objs:
            print("- %s") % (str(feat))
        print("\nClassifiers used:")
        for cl in classif_objs:
            print("- %s") % (str(cl))
        print("")

    # extract features and build a list of instances
    instances, labels = extract_instances(dataset, feat_objs)

    # TODO : make the feature selection optional
    fs.FeaturesSelection.chi2(instances, labels)

    print("\nEntropy of the labels:")
    print(u.entropy(labels))
    print("")

    if classification:
        size         = int(math.floor(len(instances)*0.25))
        train_data   = instances[0:-size+1]
        test_data    = instances[-size+1:]
        train_labels = labels[0:-size+1]
        test_labels  = labels[-size+1:]

        if multiprocessing:
            c_thread = Process(target=classification_routine,
                               args=(train_data, test_data, train_labels,
                                     test_labels, classif_objs))
            print("Starting classification thread...")
            c_thread.start()
        else:
            classification_routine(train_data, test_data, train_labels,
                                   test_labels, classif_objs)

    if x_validation:
        if multiprocessing:
            xv_thread = Process(target=cross_validation,
                                args=(instances, labels, classif_objs))
            print("Starting cross-validation thread...")
            xv_thread.start()
        else:
            ave,_,_ = cross_validation(instances, labels, classif_objs)
            print('average accuracy :')
            print(ave)

    if tournament:
        if multiprocessing:
            t_thread = Process(target=algorithm_tournament,
                               args=(instances, labels, classif_objs))
            print("Starting tournament thread...")
            t_thread.start()
        else:
            algorithm_tournament(instances, labels, classif_objs)

    if multiprocessing:
        if classification:
            c_thread.join()
        if x_validation:
            xv_thread.join()
        if tournament:
            t_thread.join()

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
    parser.add_argument('-d', '--devset',
                        action='store_true',
                        default=False,
                        help='use development dataset')
    parser.add_argument('-m', '--multiprocessing',
                        action='store_true',
                        default=False,
                        help='activate multiprocessing. It should be faster on \
                        a machine with multiple cpu/cores but the messages \
                        from the program will be printed randomly.')
    parser.add_argument('-r', '--randomize',
                        action='store_true',
                        default=False,
                        help='randomize dataset')
    parser.add_argument('-t', '--tournament',
                        action='store_true',
                        default=False,
                        help='perform algorithm tournament')
    parser.add_argument('-p', '--plot-roc',
                        action='store_true',
                        default=False,
                        help='plot ROC curve')
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

    if not (args.all or
            args.classification or
            args.tournament or
            args.x_validation):
        print("No option chosen. Thus simply performing classification.")
        main(True,
             args.tournament,
             args.x_validation,
             args.devset,
             args.randomize,
             args.verbose,
             args.plot_roc,
             args.multiprocessing)
    elif args.all:
        main(True,
             True,
             True,
             args.devset,
             args.randomize,
             args.verbose,
             args.plot_roc,
             args.multiprocessing)
    else:
        main(args.classification,
             args.tournament,
             args.x_validation,
             args.devset,
             args.randomize,
             args.verbose,
             args.plot_roc,
             args.multiprocessing)

    sys.exit(0)
