from Classes.AbstractWorld import AbstractWorld
import random
import pygame
import numpy as np
import queue
import math
from _collections import defaultdict
pygame.font.init() 
from Classes.Order import Order
import copy
import heapq
from collections import deque
from Classes.ProductionLines import ProductionLines
from Classes.Warehouses import Warehouses

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
        self.profit = 0
        self.costs = self.get_costs() #dictionary with key - set of nodes, value - cost to go between
        self.preList = self.set_paths() #dictionary with key - start node, value - predacessor dictionary to recreate paths
        self.productionLines = self.set_productionLines2(self.getProductionLines()) #dictionary with key - type of line and value - list of production line objects
        self.warehouses = self.set_warehouses(self.getLocationOfWarehouses()) #dictionary with key - type of material at warehouse and value - list of warehouse objects
        self.van = pygame.image.load("mysteryMachine.png").convert() #van load the image
        self.van = pygame.transform.scale(self.van, (10,10)) #scale the van for animation
        self.trucks = None #the trucks included in the world
        
    def get_coordinates(self): #method to create the coordinate dictionary
        coords = {} #initialize
        for i in self.Verticies: #go through vertices
            coords[i[0]] = (i[1],i[2]) #add coordinates
        return coords #return the dictionary
    
    def get_costs(self): #method to create costs dictionary
        maxCost =0
        edge = None
        costs = defaultdict(lambda: 1000) #default dic w lambda at "infinity"
        costForTrain = {}
        for i in self.Edges: #go through edges
            costs[(i[0],i[1])] = i[2] #put in the cost
            costs[(i[1],i[0])] = i[2]
            if i[4] == 'B':
                print ("i: ", i)
                print("i2: ", i[2])
                costForTrain[(i[0],i[1], i[2])] = i[2] #put in the cost
        for i in self.Verticies: #go through verticies
            costs[(i[0], i[0])] = 0 #cost from self to self
        totalSpending = 0
        '''
        while totalSpending <= 100000000 and costForTrain[max(costForTrain.keys())] > 2:
            totalSpending += costForTrain[max(costForTrain.keys())]*1000000
            if totalSpending > 100000000:
                break
            self.profit -= costForTrain[max(costForTrain.keys())]*1000000
            max(costForTrain.keys())[2] = 2
            costs[(max(costForTrain.keys())[0], max(costForTrain.keys())[1])] = 2
            costs[(max(costForTrain.keys())[1], max(costForTrain.keys())[0])] = 2
        '''
        print ("this guy: ", costs[max(costs.keys())])
        print("that guy: ", max(costs.keys()))
        print(costs[(229,229)])
        print("Costs: ", costs)
        while totalSpending <= 100000000 and costs[max(costs.keys())] > 2:
            totalSpending += costs[max(costs.keys())]*1000000
            if totalSpending > 100000000:
                break
            self.profit -= costs[max(costs.keys())]*1000000
            edge = None
            for i in self.Edges:
                if max(costs.keys())[0] == i[0] and max(costs.keys())[1] == i[1]:
                    edge = i
                    break
            edge[2] = 2
            costs[(max(costs.keys())[0], max(costs.keys()[1]))] = 2
            costs[(max(costs.keys())[1], max(costs.keys()[0]))] = 2
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
    
    def get_path_length(self, path): # method to get the length of the path
        pathLength = 0
        for i in range(len(path)-1):
            pathLength += self.costs[(path[i], path[i+1])]
        return pathLength
    
    def set_productionLines2(self, lineList):
        for i in lineList:
            line = ProductionLines(i['type'], i['location'], i['capacityOfMaterial[tons]'])
        line = ProductionLines()
        return line.get_linesdic()
    
    def set_warehouses(self, warehouseList):
        for i in warehouseList:
            whouse = Warehouses(i['type'], i['location'])
        whouse = Warehouses()
        return whouse.get_warehousedic()
    
    
    
    def find_vehicle(self, trucks):
        return random.choice(trucks)
    
    def get_production(self, object):
        return object.productionProcess

    def runSimulation(self, fps=5, initialTime=5*60, finalTime=23*60):

        '''
        This will give you a list of ALL cars which are in the system
        '''
        ''
        trucks = self.getInitialTruckLocations()
        self.trucks = trucks
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
            pygame.draw.rect(self.screen, (255,0,0), ((self.width*self.Verticies[i][1]/maxX)*self.scale - 5, (self.height*self.Verticies[i][2]/maxY)*self.scale - 5, 10, 10))
          
        for j in range(len(self.Edges)):
            for k in range(len(self.Edges[j][3]) - 1):
                pygame.draw.line(self.screen, (255,0,0), 
                                 ((self.width*self.Edges[j][3][k][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k][1]/maxY)*self.scale), 
                                  ((self.width*self.Edges[j][3][k+1][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k+1][1]/maxY)*self.scale), 2)
    
        vehicles = {}
        
        currentOrders = [] #list to hold all the current orders
        currentTrucks = []
        finishedOrders = []
        
        for i in range(len(trucks)):
            vehicles[round((trucks[i].ID)/3)] = queue.Queue()
        
        for t in range(initialTime,finalTime):    
            print("\n\n Time: %02d:%02d"%(t/60, t%60))
            print("T: ", t)
            # each minute we can get a few new orders
            newOrders = self.getNewOrdersForGivenTime(t) #get the new orders
            num = len(newOrders) #get number of new orders
            #print("NEW ORDERS: ", newOrders)
            # create lists to hold the starting and ending vertex of the orders
            for i in newOrders: #go through all new orders
                #set the starting (random) and ending (given)
                i.set_start_time(t)
                print ("PROD PROCESS: ", i.getProductionProcess())
                values = self.get_production(i)
                #print("WAREHOUSES (me): ", self.warehouses)
                #print("PRODUCTION LINES (me): ", self.productionLines)
                i.setEnd(i.getFinalLocation()) #end is final location
                i.setStart(random.choice(self.Verticies)) #start is random
                #assign a truck to the order
                orderTruck = self.get_truck_for_order(i.getStart()) #get the truck closest to start
                i.setTruck(orderTruck) #set the order's truck
                orderTruck.add_order(i) #add the order to the truck
                currentTrucks.append(i.getTruck())
                fullPath=deque() #initialize list to hold full path of order
                locationPath = self.get_location_path(i)
                #print("LOCATION PATH: ", locationPath)
                #print("TRUCKS: ", trucks)
                for j in range(len(locationPath)-1): #go through all but last
                    if locationPath[j][0] == locationPath[j+1][0]: #if they are the same
                        fullPath.append(locationPath[j][0]) #add a copy of the path to the list
                    else:
                        tempPath = self.get_path(locationPath[j][0], locationPath[j+1][0]) #get path from current to next location
                        if j!= 0: #if not the first
                            del tempPath[0] #remove first node in path so we don't double count it
                        fullPath += tempPath #combine the temporary path with the full path
                i.setPath(fullPath)
                coordPath = (i.getTruck()).add_path(fullPath, self.costs, self.coord, i.getID()) #add the path for the order to the path for the truck
                i.setCoordPath(coordPath)
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

            self.screen.fill((0,0,0))
            for k in self.coord: #for each vertex
                x = self.coord[k][0] #get x and y coordinates
                y = self.coord[k][1]
                #redraw the red rectangle
                pygame.draw.rect(self.screen, (255,0,0), 
                                 ((self.width*x/maxX)*self.scale - 5, 
                                  (self.height*y/maxY)*self.scale - 5, 10, 10))
            for j in range(len(self.Edges)):
                for k in range(len(self.Edges[j][3]) - 1):
                    pygame.draw.line(self.screen, (255,0,0), 
                                 ((self.width*self.Edges[j][3][k][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k][1]/maxY)*self.scale), 
                                  ((self.width*self.Edges[j][3][k+1][0]/maxX)*self.scale, (self.height*self.Edges[j][3][k+1][1]/maxY)*self.scale), 2)
       
            #DRAWING THE MOVING ORDERS AS WHITE
            for k in trucks: #go through current orders
                path = k.get_coordPath() #get the path of the truck as a queue
                if len(path) != 0: #if the truck's path isn't empty
                    #print ("PATH: ", path)
                    currentVertex = path.popleft() #get the first item in the path
                    #print("CURRENT VERTEX", currentVertex)
                    if currentVertex[1] == 1 or currentVertex[1] == 2: #if we are at a node or the end of the order
                        truckVertex = (k.get_path()).popleft() #pop the leftmost node
                        k.set_position(truckVertex)
                        if currentVertex[1] == 2:
                            order = k.get_current_order()
                            #print ("order ID: ", order.getID())
                            print("COORD PATH: ", order.getCoordPath())
                            currentOrders.remove(order)
                            finishedOrders.append(order)
                            #print("ORDER TIME: ", t-order.get_start_time())
                            #pygame.time.delay(3000)
                            if t - order.get_start_time() >= 90:
                                order.add_cost(100000 + 100000*((t-order.get_start_time())-90)//30)
                            self.profit = self.profit + 1500000 - order.get_cost()
                                
                    x = currentVertex[0][0] #get the coordinates of the current vertex
                    y = currentVertex[0][1]
                    #pygame.time.delay(500)
                    self.screen.blit(self.van, ((self.width*x/maxX)*self.scale - 5, 
                                      (self.height*y/maxY)*self.scale - 5))
            
            #print ("profit: ", profit)
            text2 = self.font.render("Profit: $%02d"%(self.profit), True, (255, 0, 0), (255, 255, 255))
            textrect2 = text.get_rect()
            textrect2.centerx = 600
            textrect2.centery = 30

            print("CURRENT ORDERS: ", currentOrders)
            print("FINISHED ORDERS: ", finishedOrders)

            self.screen.blit(text, textrect)
            self.screen.blit(text2, textrect2)
 
            
            '''
            You should plot the vetricies, edges and cars and customers
            Each time, cars will move and you should visualize it 
            accordingly
            '''
     
            pygame.display.update()
            for event in pygame.event.get():
                pass   
            self.clock.tick(fps)
            
        print ("FINAL PROFIT: ", profit)
            
    def get_truck_for_order(self, orderStart): #method to find the nearest truck to an order
        truckPath = None
        truckChoice = None
        counter = 0 #counter to see if any trucks aren't busy
        for i in self.trucks: #go through all the trucks
            if len(i.get_coordPath()) == 0: # look at trucks that aren't currently busy
                counter+=1 #increment counter
                path = self.get_path(orderStart, i.get_position()) #get a path from order to truck position
                pathL = self.get_path_length(path)
                if truckPath == None or pathL < self.get_path_length(truckPath):
                    truckPath = path
                    truckChoice = i
        if counter == 0: #if there were no non busy trucks
            pathLength = 10000 #initialize length to super high
            for i in self.trucks: #go through all trucks
                length = len(i.get_coordPath()) #get all the points the truck has to go on
                if length < pathLength: #check if this truck has less coordinates to traverse
                    pathLength = length
                    truckChoice = i
        return truckChoice
    
    def get_location_path(self, order):
        locationPath = deque()
        pathToStart = None
        #put in the truck's initial location
        if len(order.truck.get_path()) == 0: #if the path isn't already on the go
            locationPath.append([order.truck.get_position(), 'truckOnWay']) #it will start at it's current position
            pathToStart = self.get_path(order.truck.get_position(), order.getStart())
        else: #if it is already in route somewhere
            locationPath.append([order.truck.get_path()[-1], 'truckOnWay']) #it will start when it ends it's last route
            pathToStart = self.get_path(order.truck.get_path()[-1], order.getStart())
        toOrderStartLength = self.get_path_length(pathToStart)
        order.add_cost(toOrderStartLength*50) #cost of moving truck to start of order with no materials
        #put in the start
        locationPath.append([order.getStart(), 'orderStart'])
        #put in each of the lines
        lineChoice = None
        for i in order.getProductionProcess(): #go through each step of the production process
            #figure out which warehouses to go to by shortest path
            resourceNeeded = i['resourceNeeded'] #get the resource needed for the process
            warehouseOptions = self.warehouses[resourceNeeded] #get a list of the warehouses with needed material
            warehousePath = None #initialize path to warehouse
            warehouseChoice = None #initialize choice of warehouse
            for j in warehouseOptions: #go through all the options
                path = self.get_path(locationPath[-1][0], j.get_location())
                pathL = self.get_path_length(path)
                if warehousePath == None or pathL < self.get_path_length(warehousePath): #if first or if the length is shorter than the current shortest
                    warehousePath = path #set the shortest to current path
                    warehouseChoice = j #set the warehouse to the current warehouse
            toWarehousePathLength = self.get_path_length(warehousePath) #get cost to move to warehouse
            order.add_cost(toWarehousePathLength*50) #cost of moving truck to warehouse with no materials
            assignedWarehouseLocation = warehouseChoice.get_location() #get location of closest warehouse
            locationPath.append([assignedWarehouseLocation, 'warehouse']) #append the nearest warehouse
            #figure out which line to go to by shortest path
            lineOptions = self.productionLines[i['processinLine']] #get lines that match the process needed
            linePath = None #initialize path to line and choice of line
            for j in lineOptions: #go through all the options
                path = self.get_path(locationPath[-1][0], j.get_location()) #get the path to each one
                pathL = self.get_path_length(path)
                if linePath == None or pathL < self.get_path_length(linePath): #if the first or the length is shorter
                    linePath = path #set the line path to the shortest path
                    lineChoice = j #set the choice of line
            toLinePathLength = self.get_path_length(linePath)
            order.add_cost(toLinePathLength*(50+5*i['materialNeeded[tons]']))
            assignedLineLocation = lineChoice.get_location() #
            locationPath.append([assignedLineLocation, 'line']) #append location of line
            for j in range(i['processingTime']): #add the location multiple times to represent processing time
                locationPath.append([assignedLineLocation, 'line'])
        
        pathToEnd = self.get_path(lineChoice.get_location(), order.getFinalLocation())
        toOrderEndLength = self.get_path_length(pathToEnd)
        order.add_cost(toOrderEndLength*50) #cost of moving truck to end location
        
        #put in the end
        locationPath.append([order.getFinalLocation(), 'orderEnd'])
        order.setLocationPath(locationPath)
        #print ("TRANSPORTATION COST FOR ORDER: ", order.get_cost())
        return locationPath
        