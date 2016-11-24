import random
import pprint
import types
import numpy as np
import pandas as pd
from IPython.core.debugger import Tracer
from collections import defaultdict
from operator import itemgetter

import lsh_tester
import lsh_index

from lsh_index import LSHIndex
from lsh_tester import LSHTester

class L2HashFamily:

    def __init__(self,w,d):
        """ d: dimenesion
            w: scale factor
        """
        self.w = w
        self.d = d

    def create_hash_func(self):
        # each L2Hash is initialised with a different random projection vector and offset
        return L2Hash(self.rand_vec(),self.rand_offset(),self.w)

    def rand_vec(self):
        return [random.gauss(0,1) for i in xrange(self.d)]

    def rand_offset(self):
        return random.uniform(0,self.w)

    def combine(self,hashes):
        """
        combine hash values naively with str()
        - in a real implementation we can mix the values so they map to integer keys
        into a conventional map table
        """
        return str(hashes)

class L2Hash:

    def __init__(self,r,b,w):
        self.r = r
        self.b = b
        self.w = w

    def hash(self,vec):
        return int((dot(vec,self.r)+self.b)/self.w)

def L2_norm(u,v):
        return sum((ux-vx)**2 for ux,vx in zip(u,v))**0.5
    
def dot(u,v):
    return sum(ux*vx for ux,vx in zip(u,v))