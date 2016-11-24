import random
import pprint
import types
import numpy as np
import pandas as pd
from IPython.core.debugger import Tracer
from collections import defaultdict
from operator import itemgetter

class CosineHashFamily:

    def __init__(self,d):
        self.d = d

    def create_hash_func(self):
        # each CosineHash is initialised with a random projection vector
        return CosineHash(self.rand_vec())

    def rand_vec(self):
        return [random.gauss(0,1) for i in xrange(self.d)]

    def combine(self,hashes):
        """ combine by treating as a bitvector """
        return sum(2**i if h > 0 else 0 for i,h in enumerate(hashes))

class CosineHash:

    def __init__(self,r):
        self.r = r

    def hash(self,vec):
        return self.sgn(dot(vec,self.r))

    def sgn(self,x):
        return int(x>0)

def cosine_distance(u,v):
    return 1 - dot(u,v)/(dot(u,u)*dot(v,v))**0.5

def dot(u,v):
    return sum(ux*vx for ux,vx in zip(u,v))