# coding: utf-8

def format_for_nltk(labels, dataset):
    if len(labels) != len(dataset):
        return []
    return [(v, labels[i]) for i,v in enumerate(dataset)]

def accuracy(labels, predictions):
    if len(labels) != len(predictions):
        return -1

    correct = 0
    total   = 0

    for i,v in enumerate(predictions):
        if labels[i] == v:
            correct += 1
        total += 1

    return (float(correct) / float(total)) * 100
