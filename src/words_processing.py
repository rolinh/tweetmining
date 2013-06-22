import re
import numpy
import nltk

from sklearn.feature_extraction.text import TfidfTransformer

def remove_html_chars(text):
    return re.sub(r'&[a-zA-Z]+;', '', text)

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
    """ Removes html chars, retweets, urls and stopwords from `text`"""
    text = remove_html_chars(text)
    text = remove_retweets(text)
    text = remove_urls(text)
    text = remove_stopwords(text).lower()
    text = text.encode('ascii', 'ignore')
    return text


def filter_tweet_words(tweet):
    filtered_words = []
    tokeep = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS',
              'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    text = preprocessing(tweet.text)
    token = nltk.word_tokenize(text)
    tags = nltk.pos_tag(token)

    for tag in tags:
        if tag[1] in tokeep:
            filtered_words.append(tag[0])
    return filtered_words

def text_as_corpus(dataset):
    """Build a corpus (without unsignificant words) of from tweets"""

    corpus = []
    for tweet in dataset:
        for v in filter_tweet_words(tweet):
            corpus.append(v)

    return ' '.join(corpus)

def corpus_as_occurrences(corpus):
    """Build a dictionary that contains each word of the given corpus and
    its occurrency"""

    text = nltk.word_tokenize(corpus)
    occ = nltk.FreqDist(text)

    return occ

def tf(data):
    """Computes TF from given data where `data` is a dictionary where key is
    a word and value is its occurence. Returns a numpy array containing the
    tf_idf in the same order as values from `data`."""
    mat = numpy.asarray(data.values())
    return TfidfTransformer(use_idf=False).fit_transform(mat)

def tf_idf(data):
    """Computes TF-IDF from given data where `data` is a dictionary where key is
    a word and value is its occurence. Returns a numpy array containing the
    tf_idf in the same order as values from `data`."""
    mat = numpy.asarray(data.values())
    return TfidfTransformer(use_idf=False).fit_transform(mat)

