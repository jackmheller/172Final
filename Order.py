#from Classes.Vehicle import Vehicle
from Classes.AbstractOrder import AbstractOrder
from random import random
import numpy as np
import queue


class Order(AbstractOrder):
    
    def __init__(self, id):
        AbstractOrder.__init__(self, id)
        self.start =  None
        self.end = None
        self.path = None
        
    def getID(self):
        return self.id
    
    def getPath(self):
        return self.path
    
    def setStart(self, vertex):
        self.start = vertex
        
    def setEnd(self, vertex):
        self.end = vertex
        
    def setPath(self, graph):
        s = self.start[0]
        e = self.end[0]
        q = [[s]] #create a list that starts with just the start node
        visited = set() #create a set to hold the visited nodes
        
        while q: #while there are still lists in the queue
            path = q.pop(0) #path is the first element
            
            vertex = path[-1] #the vertex is the last point in the path
            
            if vertex == e: #if we are at the end
                self.path = queue.Queue() #create a queue object to hold path
                self.path.queue = queue.deque(path) #convert list to queue object
                return #return the queue
            elif vertex not in visited: #if the vertex hasn't been visited
                for neighbor in graph[vertex]: #go through the neighbors of the vertex
                    new_path= list(path) #make path into a list
                    new_path.append(neighbor) #add the neighbor to the new path
                    q.append(new_path) #put this path with a neighbor into the queue
            visited.add(vertex) #note that we visited the vertex

