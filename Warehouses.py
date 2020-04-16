'''
Created on Apr 16, 2020

@author: sophiesmith
'''
from _collections import defaultdict

class Warehouses():
    warehouseDictionary= defaultdict(list) #dictionary to hold instances of each type of warehouse
    def __init__(self, type=None, location=None):
        self.type = type
        self.location = location
        self.warehouseDictionary[self.type].append(self)
        
    def get_warehousedic(self): #return the dictionary of warehouses
        return self.warehouseDictionary
    
    def get_location(self): #return the location of the warehouse
        return self.location