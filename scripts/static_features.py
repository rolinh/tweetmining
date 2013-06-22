#!/usr/bin/env python
# coding: utf-8

import sys
import os
import re
import codecs
import nltk

sys.path.insert(0, os.path.abspath('../src'))

import utils as u

def remove_retweets(text):
    return re.sub(r'RT @.+: ', '', text)

def remove_urls(text):
    return re.sub(r'https?:\/\/t\.co\/[a-zA-Z0-9]+', '', text)

def remove_stopwords(text):
    chars = ['.', '/', "'", '"', '?', '!', '#', '$', '%', '^', '&', '*', '(',
             ')', ' - ', '_', '+' ,'=', '@', ':', '\\', ',', ';', '~', '`', '<',
             '>', '|', '[', ']', '{', '}', '"', '-',]
    for c in chars:
        text = text.replace(c, ' ')

    text = text.split()

    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower().strip() not in stopwords]
    return ' '.join(content)

def preprocessing(text):
    text = remove_retweets(text)
    text = remove_urls(text)
    text = remove_stopwords(text).lower()
    text = text.encode('ascii', 'ignore')
    return text

def text_as_corpus(dataset):
    """Build a corpus (without unsignificant words) of from tweets"""

    corpus = []
    tokeep = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS',
              'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    for tweet in dataset:
        text = preprocessing(tweet.text)
        token = nltk.word_tokenize(text)
        tags = nltk.pos_tag(token)

        for tag in tags:
            if tag[1] in tokeep:
                corpus.append(tag[0])

    return ' '.join(corpus)

def corpus_as_frequencies(corpus):
    """Build a dictionary that contains each word of the given corpus and
    its frequency"""

    text = nltk.word_tokenize(corpus)
    freq = nltk.FreqDist(text)

    return freq

outfile = '../data/dataset_words_freq.txt'

print("Collecting data...")
dataset = u.json_to_tweets('../data/dataset.json', False)

print("Extracting words frequencies...")
corpus = text_as_corpus(dataset)
word_freq = corpus_as_frequencies(corpus)

print("Writing to file %s") % outfile
f = codecs.open(outfile, 'w', 'utf-8')
for k,v in word_freq.items():
    line = k + ":" + str(v) + "\n"
    f.write(line)
f.close()

