import random
import pprint
import types
import numpy as np
import pandas as pd
from IPython.core.debugger import Tracer
from collections import defaultdict
from operator import itemgetter

import l2_hash_family
import lsh_tester

# from l2_hash_family import L2HashFamily
# from lsh_tester import LSHTester

class LSHIndex:

    def __init__(self,hash_family,k,L):
        self.hash_family = hash_family
        self.k = k
        self.L = 0
        self.hash_tables = []
        self.resize(L)

    def resize(self,L):
        """ update the number of hash tables to be used """
        if L < self.L:
            self.hash_tables = self.hash_tables[:L]
        else:
            # initialise a new hash table for each hash function
            hash_funcs = [[self.hash_family.create_hash_func() for h in xrange(self.k)] for l in xrange(self.L,L)]
            # Tracer()()
            # pprint.pprint(hash_funcs)
            self.hash_tables.extend([(g,defaultdict(lambda:[])) for g in hash_funcs])
            # hf = pd.DataFrame(hash_funcs)
            # pprint.pprint(hf, width= 200)

    def hash(self,g,p):
        return self.hash_family.combine([h.hash(p) for h in g])

    def index(self,points):
        """ index the supplied points """
        self.points = points
#         Tracer()()
        """ g is random projection, num(g) = k """
        """ ix is index of x which the index of original points array"""
        """ p is points """
        """ hash(g,p) is hash index return by hash function """
        """ table is array: table[x] = y: x is hash index -> y is points index (ix) """
        for g,table in self.hash_tables:
#             print "g:"
#             for gg in g: pprint.pprint(gg.__dict__)
            for ix,p in enumerate(self.points):
                table[self.hash(g,p)].append(ix)
#             print "table:"
#             pprint.pprint(table)
        # reset stats
        self.tot_touched = 0
        self.num_queries = 0

    def query(self,q,metric,max_results):
        """ find the max_results closest indexed points to q according to the supplied metric """
        candidates = set()
        for g,table in self.hash_tables:
            matches = table.get(self.hash(g,q),[])
            candidates.update(matches)
        # update stats
        self.tot_touched += len(candidates)
        self.num_queries += 1
        # rerank candidates
        candidates = [(ix,metric(q,self.points[ix])) for ix in candidates]
        candidates.sort(key=itemgetter(1))
        return candidates[:max_results]

    def get_avg_touched(self):
        """ mean number of candidates inspected per query """
        return self.tot_touched/self.num_queries