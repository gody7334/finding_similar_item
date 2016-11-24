import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.util import ngrams

punctuations = list(string.punctuation)
punctuations.extend(["``", "--", "''"])
sw=set(stopwords.words('english'))

def char_token(text, n=9):
    tokens_set = set()
    tokens_list = list(text)
    ngram_gen = list(ngrams(tokens_list,n))
    for grams in ngram_gen:
        ngram_token = ''.join(grams)
        tokens_set.add(ngram_token)
    return tokens_set

def word_token(text, n=5):
    tokens_set = set()
    tokens_list = nltk.word_tokenize(text)
    tokens_list = list([i for i in tokens_list if i not in punctuations])
    ngram_gen = list(ngrams(tokens_list, n))
    for grams in ngram_gen:
        ngram_token = ' '.join(grams)
        tokens_set.add(ngram_token)
    return tokens_set
        
def simple_space_token(text, n=5):
    tokens_set = set()
    tokens_list = text.split(" ")
    ngram_gen = ngrams(tokens_list, n)
    for grams in ngram_gen:
        ngram_token = ' '.join(grams)
        tokens_set.add(ngram_token)
    return tokens_set

def remove_stop_word_punc_token(text, n=5):
    tokens_set = set()
    tokens_list = nltk.word_tokenize(text)
    tokens_list = [i for i in tokens_list if i not in punctuations]
    tokens_list = filter(lambda w: not w.lower() in sw,tokens_list)
    ngram_gen = ngrams(tokens_list, n)
    for grams in ngram_gen:
        ngram_token = ' '.join(grams)
        tokens_set.add(ngram_token)
    return tokens_set
        
def stemming_token(text, n=5):
    tokens_set = set()
    porter_stemmer = PorterStemmer()
    tokens_list = nltk.word_tokenize(text)
    tokens_list = [i for i in tokens_list if i not in punctuations]
    tokens_list = filter(lambda w: not w.lower() in sw,tokens_list)
    tokens_list = [porter_stemmer.stem(w) for w in tokens_list]
    ngram_gen = ngrams(tokens_list, n)
    for grams in ngram_gen:
        ngram_token = ' '.join(grams)
        tokens_set.add(ngram_token)
    return tokens_set

def jaccard_similarity(set1, set2):
    j_s = float(len(set1.intersection(set2))) / float(len(set1.union(set2)))
    return j_s
