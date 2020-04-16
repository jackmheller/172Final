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
        self.coordPath = deque()
        
    def get_position(self):
        return self.currentVertex
    
    def get_coordPath(self):
        return self.coordPath
    
    def get_capacity(self):
        return self.capacity
    
    def get_current_order(self):
        order = self.orders.popleft()
        return order
    
    def get_edge_points(self, currentVertex, nextVertex, cost, coord, last): #get points to animate between vertices
        points = [] #initialize array to hold points
        xCurrent = coord[currentVertex][0] #get the coordinates of the current vertex
        yCurrent = coord[currentVertex][1]
        xNext = coord[nextVertex][0] #get coordinates of next vertex
        yNext = coord[nextVertex][1]
        if currentVertex == nextVertex: #if the vertex is the same
            if last == False: #if not last in order
                points.append([(xCurrent, yCurrent), 1]) #return coordinates of point with 1 (at vertex, not end of order)
            else: #if last point in order
                points.append([(xCurrent, yCurrent), 2]) #return coordinates of point with 2 (at vertex AND end of order)
            return points #return the points
        if cost[(currentVertex, nextVertex)] == 1: #if the cost is one
            points.append([(xCurrent, yCurrent), 0]) #append the first position with 0 (since it will be deleted from first and have 1 in previous path)
            if last == False: #check if last vertex in order
                points.append([(xNext, yNext), 1]) #append coordinates of point with 1 (at vertex, not end of order)
            else:
                points.append([(xNext, yNext), 2]) #append coordinates of point with 2 (at vertex AND end of order)
            return points #return points
        direction = (xNext - xCurrent, yNext - yCurrent) #slope of line
        points.append([(xCurrent, yCurrent), 0]) #put the first vertex in
        for i in range(cost[(currentVertex, nextVertex)] - 2): #go up to the coordinate before the last one
            xLocation = xCurrent + (i+1)*direction[0]/cost[(currentVertex, nextVertex)] #current location
            yLocation = yCurrent + (i+1)*direction[1]/cost[(currentVertex, nextVertex)]
            points.append([(xLocation, yLocation), 0]) #add point with 0 (not at a vertex)
        if last == False: #check if at last vertex in an order
            points.append([(xNext, yNext), 1]) #append coordinates of point with 1 (at vertex, not end of order)
        else:
            points.append([(xNext, yNext), 2]) #append coordinates of point with 2 (at vertex AND end of order)
        return points
            
    def add_path(self, newPath, cost, coord): #method to add the path of vertices/coordinates for each new order
        newPath.popleft() #remove the duplicate element
        self.path += newPath #add the new path to the path of the truck
        fullPath = deque() #deque to hold the full coordinate path of the new path
        for n in range(len(newPath) - 1): #go through all the new points in the path
            tempPath = deque() #initialize a deque to hold new path
            if n != len(newPath)-2: #if we aren't at the last point in the new path (last point in the order's path)
                tempPath = self.get_edge_points(newPath[n], newPath[n+1], cost, coord, False) #get points with last as false
            else: #if at the last point in the order
                tempPath = self.get_edge_points(newPath[n], newPath[n+1], cost, coord, True) #get points with last as true
            if n != 0 and len(tempPath) != 1: #if not the first points and the length of the temporary path isn't 1
                del tempPath[0] #delete the first element so it's not double counted
            fullPath += tempPath #add temp path to full path
        self.coordPath += fullPath #add the full path to the coordinates the truck goes over
        
    def get_path(self): #return the path of vertices for the truck
        return self.path
    
    def set_position(self, v):
        self.currentVertex = v
        
    def add_order(self, order):
        self.orders.append(order)
        
    def remove_order(self, orderNum):
        self.orders.remove(orderNum)
        
    def get_orders(self):
        return self.orders
