from Classes.Vehicle import Vehicle
from Classes.AbstractOrder import AbstractOrder
from random import random
import numpy as np


class Order(AbstractOrder):
    
    def __init__(self, id):
        AbstractOrder.__init__(self, id)
        self.start = random.choice(World.get_vert())
        self.end = random.choice(World.get_vert())
        if self.start == self.end:
            self.end = random.choice(World.get_vert())
        
'''
    def path(self, start_node, end_node):
        g = Graph()
        d = {} # this will store the "distances from start_node"
        for v in g.neighbors:
            d[v] = np.Inf
        d[start_node] = 0
        smallest_node =  start_node 
        permanent = {}
        pre={}
        while smallest_node!= end_node: #Question #1: How many times this can happen? 
            smallest_value = np.Inf 
            smallest_node = None 
            for v in d: # we are searching for the smallest "label" which is not permanent
                if v not in permanent and (d[v] < smallest_value):
                    smallest_value = d[v]
                    smallest_node = v
            permanent[smallest_node] = True # I am denoting this node with smallest d[v] value as "final" / permanent
            for nv in g.neighbors[smallest_node]: # checking neighbours of "smallest_node" ....
                if nv not in permanent:  # Question #2: is this check "important"? Would it work if I remove it? 
                    proposed_distance = d[smallest_node] + g.get_cost(smallest_node, nv)
                    if proposed_distance < d[nv]: # if new path via node smallest_node is better, update "d"
                        d[nv] = proposed_distance
                        pre[nv] = smallest_node
        return pre
'''
