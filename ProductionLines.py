'''
Created on Apr 2, 2020

@author: sophiesmith
'''

from _collections import defaultdict

class ProductionLines():
    linesDictionary= defaultdict(list) #dictionary to hold instances of each type of production line
    def __init__(self, type=None, location=None, capacity=None):
        self.type = type
        self.location = location
        self.capacity = capacity
        self.busy = False
        self.currentMaterials = self.capacity
        self.locationPath = [] #list to hold path of locations order must go
        self.linesDictionary[self.type].append(self)
        
    def get_linesdic(self): #return the dictionary of lines
        return self.linesDictionary
    
    def get_location(self): #return the location of the line
        return self.location