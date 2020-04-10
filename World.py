from Classes.AbstractWorld import AbstractWorld
import random
import pygame
import numpy as np
from networkx.classes.function import neighbors
import queue
import math
from _collections import defaultdict
from anaconda_navigator.app import start
from networkx.algorithms.assortativity import neighbor_degree
pygame.font.init() 
from Classes.Order import Order
import copy
import heapq
from collections import deque
from Classes.ProductionLines import ProductionLines

class World(AbstractWorld):
    
    def __init__(self):
        AbstractWorld.__init__(self)
        self.scale = 0.5
        self.height = 600
        self.width = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.black = (0,0,0)
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont('Comic Sans MS', 30)
        self.pred = {} #holds paths between all sets of nodes
        self.graph = self.get_neighbors() #dictionary with key - node, value - list of neighbors
        self.coord = self.get_coordinates() #dictionary with key - node, value - coords
        self.costs = self.get_costs() #dictionary with key - set of nodes, value - cost to go between
        self.preList = self.set_paths() #dictionary with key - start node, value - predacessor dictionary to recreate paths
        self.productionLines = self.set_productionLines2(self.getProductionLines()) #dictionary with key - type of line and value - list with [ID, location, material capacity]
        self.van = pygame.image.load("mysteryMachine.png").convert()
        self.van = pygame.transform.scale(self.van, (10,10))
        
    def get_coordinates(self): #method to create the coordinate dictionary
        coords = {} #initialize
        for i in self.Verticies: #go through verticies
            coords[i[0]] = (i[1],i[2]) #add coordinates
        return coords #return the dictionary
    
    def get_costs(self): #method to create costs dictionary
        costs = defaultdict(lambda: 10000) #default dic w lambda at "infinity"
        for i in self.Edges: #go through edges
            costs[(i[0],i[1])] = i[2] #put in the cost
            costs[(i[1],i[0])] = i[2]
        for i in self.Verticies: #go through verticies
            costs[(i[0], i[0])] = 0 #cost from self to self
        return costs #return the dictionary
    
    def get_vert(self):
        return self.Verticies
    
    def get_neighbors(self): #method to get the graph dictionary
        neighbors= defaultdict(list) #initialize defaultdic of lists
        for i in self.Verticies: #go through verticies
            for j in self.Edges: #go through edges
                if j[4] == 'B': #if the edge goes both ways
                    if j[0] == i[0]: #if the vertex matches the first node in edge
                        neighbors[(i[0])].append(j[1]) #append the second node in edge to neighbors
                    if j[1] == i[0]: #if the second node in edge is vertex
                        neighbors[(i[0])].append(j[0]) #put in the first node
                elif j[4] == 'OneWayB': #if one way, starting at B
                    if j[1] == i[0]: #if the second node in edge is vertex
                        neighbors[(i[0])].append(j[0]) #add the first node
                elif j[4] == 'OneWayA': #if it's a one way edge starting at A
                    if j[0] == i[0]: #if the vertex matches the first node in edge
                        neighbors[(i[0])].append(j[1]) #append the second node in edge to neighbors
        return neighbors
    
    def set_paths(self): #get predecessor dictionary for each node 
        preList = {} #initialize dictionary to hold predecessor list for every node
        for i in self.Verticies: #go through all nodes as the start node
            start = i[0] #take the vertex number
            d = {} #dictionary to hold distances to nodes
            heap = [] #heap to store distance, node
            d[start] = 0 #set distance to start node as 0
            heapq.heappush(heap,(0,start)) #push this onto the heap
            small_node = start #set start to the smallest node
            #initialize dictionaries to hold explored nodes and predecessor lsits
            perm = {}
            pre = {}
            while len(heap) > 0: #while there are items on the heap (still haven't finished making the full predecessor list)
                small_val,small_node = heapq.heappop(heap) #pop the value and node
                if small_node in perm: #if the node has been explored
                    continue #move along
                perm[small_node] = True #set the node as explored
    
                for nv in self.graph[small_node]: #go through the neighbors
                    if nv not in perm: #if the neighbor hasn't been explored
                        proposed_dist = d[small_node] + self.costs[(small_node, nv)] #distance is the distance to the first node plus the distance to neighbor
                        if nv in d: #if the neighbor is in distances
                            if proposed_dist < d[nv]: #if the proposed distance is less than the distance to node
                                heapq.heappush(heap, (proposed_dist, nv)) #put the proposed distance and the node on the heap
                                d[nv] = proposed_dist #add the proposed distance as the node distance
                                pre[nv] = small_node #put the predecessor in the dictionary
                        else: #if not in distance 
                            heapq.heappush(heap, (proposed_dist, nv)) #add to heap
                            d[nv] = proposed_dist #set a distance
                            pre[nv] = small_node #set a predecessor
            preList[start] = pre #put the predecessor list for the node into a list
        return preList #return the dictionary with predecessor dictionaries for every node
    
    def get_path(self, start, end): #method to return a path given start and end points
        if start == end: #if we are already there
            return [start] #just return the node
        pre = self.preList[start] #get the predecessor list for the start node
        pathList = deque([end]) #put the end node in the path list
        n = None #start with no node
        while n!= start: #if n is not the start node
            n = pre[end] #set n to the predecessor to the end node
            pathList.appendleft(n) #put n at position 0 in the path
            end = n #set end to be node n
        return pathList #return the path
    
    def set_productionLines2(self, lineList):
        for i in lineList:
            line = ProductionLines(i['type'], i['location'], i['capacityOfMaterial[tons]'])
        line = ProductionLines()
        return line.get_linesdic()
    
    
    def find_vehicle(self, trucks):
        return random.choice(trucks)

    def runSimulation(self, fps=5, initialTime=5*60, finalTime=23*60):

        '''
        This will give you a list of ALL cars which are in the system
        '''
        trucks = self.getInitialTruckLocations()
        for i,t in enumerate(trucks):
            print("vehicle %d: %s"%(i, str(t)))

        '''
        We will run a simulation where "t" is the time index
        '''
        listX = []
        listY = []
        for a in range(len(self.Verticies)):
            listX.append(self.Verticies[i][1])
            listY.append(self.Verticies[i][2])
        maxX = max(listX)
        maxY = max(listY)
        for i in range(len(self.Verticies)):
            pygame.draw.rect(self.screen, (255,0,0), ((self.width*self.Verticies[i][1]/maxX)*self.scale, (self.height*self.Verticies[i][2]/maxY)*self.scale, 10, 10))
          
        for j in range(len(self.Edges)):
            for k in range(len(self.Edges[j][3]) - 1):
                print(k, len(self.Edges[j][3]))
                pygame.draw.line(self.screen, (255,0,0), 
                                 ((self.width*self.Edges[j][3][k][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k][1]/maxY)*self.scale), 
                                  ((self.width*self.Edges[j][3][k+1][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k+1][1]/maxY)*self.scale), 2)
    
        vehicles = {}
        
        currentOrders = [] #list to hold all the current orders
        currentTrucks = []
        
        for i in range(len(trucks)):
            vehicles[round((trucks[i].ID)/3)] = queue.Queue()
        
        for t in range(initialTime,finalTime):    
            print("\n\n Time: %02d:%02d"%(t/60, t%60))
            # each minute we can get a few new orders
            newOrders = self.getNewOrdersForGivenTime(t) #get the new orders
            num = len(newOrders) #get number of new orders
            # create lists to hold the starting and ending vertex of the orders
            for i in newOrders: #go through all new orders
                #set the starting (random) and ending (given)
                i.setTruck(trucks) #assign a vehicle to the order
                (i.getTruck()).add_order(i.getID()) #add the order to the truck
                currentTrucks.append(i.getTruck())
                i.setEnd(i.getFinalLocation()) #end is final location
                i.setStart(random.choice(self.Verticies)) #start is random
                i.setLocationPath(self.productionLines) #get the order of locations we go to
                fullPath=deque() #initialize list to hold full path of order
                locationPath = i.getLocationPath() #use the list of locations
                for j in range(len(locationPath)-1): #go through all but last
                    if locationPath[j] == locationPath[j+1]: #if they are the same
                        fullPath.append(locationPath[j]) #add a copy of the path to the list
                    else:
                        tempPath = self.get_path(locationPath[j], locationPath[j+1]) #get path from current to next location
                        if j!= 0: #if not the first
                            del tempPath[0] #remove first node in path so we don't double count it
                        fullPath += tempPath #combine the temporary path with the full path
                i.setPath(fullPath)
                (i.getTruck()).add_path(fullPath, self.costs, self.coord) #add the path for the order to the path for the truck
                currentOrders.append(i) #add the order to the list of current orders
            
            #print out the new orders
            print("New orders:")
            for c in newOrders:
                print(c)
            
            text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
            textrect = text.get_rect()
            textrect.centerx = 100
            textrect.centery = 30
            #self.screen.fill((255, 255, 255))
            '''
            for k in range(len(vehicles)):
                vert = vehicles.get(queue)
                if vert != None:
                    x = self.Verticies[vert][1]
                    y = self.Verticies[vert][2]
                    pygame.draw.rect(self.screen, (255,255,255), 
                                     ((self.width*x/maxX)*self.scale, 
                                      (self.height*y/maxY)*self.scale, 10, 10))
                    
            '''
            #REDRAWING THE VERTICES AS RED
            #go through each of the verticies
            self.screen.fill((0,0,0))
            for k in self.coord: #for each vertex
                x = self.coord[k][0] #get x and y coordinates
                y = self.coord[k][1]
                #redraw the red rectangle
                pygame.draw.rect(self.screen, (255,0,0), 
                                 ((self.width*x/maxX)*self.scale, 
                                  (self.height*y/maxY)*self.scale, 10, 10))
            for j in range(len(self.Edges)):
                for k in range(len(self.Edges[j][3]) - 1):
                    pygame.draw.line(self.screen, (255,0,0), 
                                 ((self.width*self.Edges[j][3][k][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k][1]/maxY)*self.scale), 
                                  ((self.width*self.Edges[j][3][k+1][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k+1][1]/maxY)*self.scale), 2)
            #go through all the order paths
            '''
            #DRAWING THE MOVING ORDERS AS WHITE
            for k in currentOrders: #go through current orders
                path = k.getPath() #get the path of the order
                if not path.empty(): #if the path isn't done
                    currentVertex = path.get() #get the first item in the path
                    x = self.coord[currentVertex][0] #get the coordinates of the current vertex
                    y = self.coord[currentVertex][1]
                    #pygame.time.delay(500)
                    if not path.qsize() == 0: #if we aren't at the last vertex
                            #draw a white square where the truck is
                        pygame.draw.rect(self.screen, (255,255,255), 
                                     ((self.width*x/maxX)*self.scale, 
                                      (self.height*y/maxY)*self.scale, 10, 10))
                        print(currentVertex)
                    else: #if we are at the last vertex
                            #print a green square so we know it's done
                        pygame.draw.rect(self.screen, (0,255,0), 
                                     ((self.width*x/maxX)*self.scale, 
                                      (self.height*y/maxY)*self.scale, 10, 10))
                else: #if the queue is empty
                    currentOrders.remove(k) #remove this order because it is done
             '''       
            #DRAWING THE MOVING ORDERS AS WHITE
            for k in trucks: #go through current orders
                #orderID = k.getID() #get the ID of the order
                #truck = k.getTruck() #get the truck carrying the order
                path = k.get_coordPath() #get the path of the truck as a queue
                #orderPath = k.getPath() #get the path of the order
                if len(path) != 0: #if the truck's path isn't empty
                    currentVertex = path.popleft() #get the first item in the path
                    #orderPath.popleft() #also remove the first element from the order path
                    k.set_position(currentVertex) #update position of the truck
                    x = currentVertex[0] #get the coordinates of the current vertex
                    y = currentVertex[1]
                    #pygame.time.delay(500)
                    #if len(orderPath) != 0: #if we aren't at the last vertex
                            #draw a white square where the truck is
                    self.screen.blit(self.van, ((self.width*x/maxX)*self.scale, 
                                      (self.height*y/maxY)*self.scale,))
                    #else: #if we are at the last vertex in an order
                            #print a green square so we know it's done
                        #pygame.draw.rect(self.screen, (0,255,0), 
                                     #((self.width*x/maxX)*self.scale, 
                                      #(self.height*y/maxY)*self.scale, 10, 10))
                        #truck.remove_order(orderID) #remove the order from the truck
                        #currentOrders.remove(k) #remove this order because it is done
                '''
                else: #if the queue is empty
                    currentOrders.remove(k) #remove this order because it is done
                '''  
            self.screen.blit(text, textrect)
            print(self.Edges)
 
            
            '''
            You should plot the vetricies, edges and cars and customers
            Each time, cars will move and you should visualize it 
            accordingly
            '''
     
            pygame.display.update()
            for event in pygame.event.get():
                pass   
            self.clock.tick(fps)
    