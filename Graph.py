'''
Created on Mar 6, 2020
@author: mayanzhe
'''
from collections import defaultdict 
from Classes.AbstractWorld import AbstractWorld


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
        

    def add_edge(self,u,v,c): #this will add edge (u,v) with cost "c" to the graph
        if u not in self.neighbors:
            self.neighbors[u]=[]
        if v not in self.neighbors:
            self.neighbors[v]=[]
        if u > v:
            u, v = v, u
        if (u,v) not in self.cost:
            self.neighbors[u].append(v)
            self.neighbors[v].append(u)
            self.cost[(u,v)] = c

    def get_cost(self, u,v):
        if u > v:
            u, v = v, u
        if (u,v) in self.cost:
            return self.cost[(u,v)]
        return None

   