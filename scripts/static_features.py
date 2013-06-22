#!/usr/bin/env python
# coding: utf-8

import sys
import os
import codecs

sys.path.insert(0, os.path.abspath('../src'))

import utils as u
import words_processing as wp

outfile = '../data/dataset_words_occurrence.txt'

print("Collecting data...")
dataset = u.json_to_tweets('../data/dataset.json', False)

print("Creating corpus...")
corpus = wp.text_as_corpus(dataset)
print("Extracting words occurrencies...")
word_occ = wp.corpus_as_occurrences(corpus)

print("Writing to file %s") % outfile
f = codecs.open(outfile, 'w', 'utf-8')
for k,v in word_occ.items():
    line = k + ":" + str(v) + "\n"
    f.write(line)
f.close()

