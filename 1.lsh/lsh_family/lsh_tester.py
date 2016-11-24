import random
import pprint
import types
import numpy as np
import pandas as pd
from IPython.core.debugger import Tracer
from collections import defaultdict
from operator import itemgetter

import l2_hash_family
import lsh_index

from lsh_index import LSHIndex
#from l2_hash_family import L2HashFamily

class LSHTester:
    """
    grid search over LSH parameters, evaluating by finding the specified
    number of nearest neighbours for the supplied queries from the supplied points
    """

    def __init__(self,points,queries,num_neighbours):
        self.points = points
        self.queries = queries
        self.num_neighbours = num_neighbours

    def run(self,name,metric,hash_family,k_vals,L_vals):
        """
        name: name of test
        metric: distance metric for nearest neighbour computation
        hash_family: hash family for LSH
        k_vals: numbers of hash (projection) to concatenates in a hash table
            numbers of hashes to concatenate in each hash function to try in grid search
            therefore, larger k, more specific region you can find
        L_vals: number of hash table
            numbers of hash functions/tables to try in grid search
            therefore, larger L, more (slightly) differernt region will be search, more points will be covered
        """
        exact_hits = [[ix for ix,dist in self.linear(q,metric,self.num_neighbours+1)] for q in self.queries]

        print name
        print 'L\tk\tacc\ttouch'
        for k in k_vals:        # concatenating more hash functions increases selectivity
            lsh = LSHIndex(hash_family,k,0)
            for L in L_vals:    # using more hash tables increases recall (increase search area, reduce false negative, and increase true positive)
                lsh.resize(L)
                lsh.index(self.points)
                # pprint.pprint(lsh.__dict__, width=200)

                correct = 0
                for q,hits in zip(self.queries,exact_hits):
                    lsh_hits = [ix for ix,dist in lsh.query(q,metric,self.num_neighbours+1)]
                    if lsh_hits == hits:
                        correct += 1
                print "{0}\t{1}\t{2}\t{3}".format(L,k,float(correct)/100,float(lsh.get_avg_touched())/len(self.points))

    def linear(self,q,metric,max_results):
        """ brute force search by linear scan """
        candidates = [(ix,metric(q,p)) for ix,p in enumerate(self.points)]
        return sorted(candidates,key=itemgetter(1))[:max_results]