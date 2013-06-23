# coding: utf-8

import sys
import os

from pyroc import *

def format_for_nltk(labels, dataset):
    """Format `labels` and `dataset` arrays to NLTK dataset format."""
    if len(labels) != len(dataset):
        return []
    return [(v, labels[i]) for i,v in enumerate(dataset)]

def format_for_scikit(labels, dataset):
    """Format `labels` and `dataset` array for Scikit dataset format."""
    nd = []
    l = [int(lab) for lab in labels]
    for i in dataset:
        tmp = [int(v) for v in i.values()]
        nd.append(tmp)
    return l,nd

def accuracy(labels, predictions, plot_roc=False):
    """Compute the accuracy of predictions"""
    if len(labels) != len(predictions):
        return -1

    correct = 0
    total   = 0

    for i,v in enumerate(predictions):
        if labels[i] == str(v):
            correct += 1
        total += 1

    if plot_roc:
        pass

    return (float(correct) / float(total)) * 100.0

def highest_bin_freq(ary):
    """Find the binary value that occurs the most frequently in a given
    array of binary values. Note that all the binary values must be given
    as a String"""
    num_true  = 0
    num_false = 0

    for val in ary:
        num_true  += 1 if val == '1' else 0
        num_false += 1 if val == '0' else 0

    return '1' if num_true > num_false else '0'

