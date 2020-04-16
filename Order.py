#from Classes.Vehicle import Vehicle
from Classes.AbstractOrder import AbstractOrder
import random
import numpy as np
import queue
import heapq
from _collections import defaultdict
from collections import deque
from Classes.ProductionLines import ProductionLines


class Order(AbstractOrder):
    def __init__(self, id):
        AbstractOrder.__init__(self, id)
        self.start =  None
        self.end = None
        self.path = None
        self.locationPath = [] #list to hold path of locations order must go
        self.truck = None
    
    #getters and setters for various attributes
    def getID(self):
        return self.id
    
    def getPath(self):
        return self.path
    
    def getStart(self):
        return self.start
    
    def getFinalLocation(self):
        return self.finalLocation
    
    def getProductionProcess(self):
        return self.productionProcess
    
    def getEnd(self):
        return self.end
    
    def getLocationPath(self):
        return self.locationPath
    
    def getGeneralPath(self):
        return self.generalPath
    
    def getTruck(self):
        return self.truck
    
    def setStart(self, vertex):
        self.start = vertex[0]
        
    def setEnd(self, vertex):
        self.end = vertex
        
    def setPath(self, path): #turn the path into a queue and set it
        #pathQ = deque(path)
        '''
        pathQ = queue.Queue() #create a queue object to hold path
        pathQ.queue = queue.deque(path) #convert list to queue object
        '''
        self.path = path
        
    def setTruck(self, trucks): #method to pick a vehicle to carry the order
        self.truck = random.choice(trucks) #randomly choose a truck
        
    def setTruck2(self, truck):
        self.truck = truck
        
    def setLocationPath(self, path):
        self.locationPath = path
