from Classes.AbstractVehicle import AbstractVehicle
from random import random
import queue
from collections import deque

class Vehicle(AbstractVehicle):
    vehicles = []
    
    def __init__(self, ID, v):
        AbstractVehicle.__init__(self,ID,v)
        self.vehicles.append(ID)
        self.path = deque() #path of the truck
        self.currentVertex = self.currentPossition[1]
        self.orders = deque() #list of orders currently on truck or in the queue
        
    def get_position(self):
        return self.currentVertex
    
    def get_capacity(self):
        return self.capacity
    
    def add_path(self, newPath):
        newPath.popleft() #remove the duplicate element
        self.path += newPath
        
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
    
    