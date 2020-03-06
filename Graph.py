'''
Created on Mar 6, 2020

@author: mayanzhe
'''
from collections import defaultdict 
from AbstractWorld import AbstractWorld


class Graph(AbstractWorld):
    def __init__(self,Vertices):
        self.graph = defaultdict(list) # default dictionary to store graph 
        self.vertices = Vertices
      
    # function to add an edge to graph 
    def addEdge(self,u,v): 
 
            self.graph[u].append(v) 
            
    # A utility function to find the subset of an element i 
    def find_parent(self, parent,i): 
        if parent[i] == -1: 
            return i 
        if parent[i]!= -1: 
            return self.find_parent(parent,parent[i]) 
  
    # A utility function to do union of two subsets 
    def union(self,parent,x,y): 
        x_set = self.find_parent(parent, x) 
        y_set = self.find_parent(parent, y) 
        parent[x_set] = y_set 
   