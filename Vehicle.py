from Classes.AbstractVehicle import AbstractVehicle
from random import random
import queue
from collections import deque
from numpy.testing._private.utils import temppath

class Vehicle(AbstractVehicle):
    vehicles = []
    
    def __init__(self, ID, v):
        AbstractVehicle.__init__(self,ID,v)
        self.vehicles.append(ID)
        self.path = deque() #path of the truck
        self.currentVertex = self.currentPossition[1]
        self.orders = deque() #list of orders currently on truck or in the queue
        self.coordPath = deque()
        
    def get_position(self):
        return self.currentVertex
    
    def get_coordPath(self):
        return self.coordPath
    
    def get_capacity(self):
        return self.capacity
    
    def get_edge_points(self, currentVertex, nextVertex, cost, coord): #get points to animate between vertices
        points = []
        xCurrent = coord[currentVertex][0] #get the coordinates of the current vertex
        yCurrent = coord[currentVertex][1]
        xNext = coord[nextVertex][0] #get coordinates of next vertex
        yNext = coord[nextVertex][1]
        if currentVertex == nextVertex:
            points.append((xCurrent, yCurrent))
            return points
        direction = (xNext - xCurrent, yNext - yCurrent) #slope of line
        if cost[(currentVertex, nextVertex)] == 1:
            points.append((xCurrent, yCurrent))
            points.append((xNext, yNext))
            return points
        for i in range(cost[(currentVertex, nextVertex)] - 1):
            xLocation = xCurrent + (i+1)*direction[0]/cost[(currentVertex, nextVertex)] #current location
            yLocation = yCurrent + (i+1)*direction[1]/cost[(currentVertex, nextVertex)]
            points.append((xLocation, yLocation))
        return points
            
    def add_path(self, newPath, cost, coord):
        newPath.popleft() #remove the duplicate element
        self.path += newPath
        fullPath = deque()
        for n in range(len(self.path) - 1):
            tempPath = deque()
            tempPath = self.get_edge_points(self.path[n], self.path[n+1], cost, coord)
            print("temp", tempPath)
            print("n", self.path[n])
            print("n+1", self.path[n+1])
            if n != 0 and len(tempPath) != 1:
                del tempPath[0]
            fullPath += tempPath
        self.coordPath += fullPath
        
    def get_path(self):
        return self.path
    
    def set_position(self, v):
        self.currentVertex = v
        
    def add_order(self, orderNum):
        self.orders.append(orderNum)
        
    def remove_order(self, orderNum):
        self.orders.remove(orderNum)
        
    def get_orders(self):
        return self.orders
