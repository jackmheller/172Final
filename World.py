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
        self.graph = self.get_neighbors()
        self.coord = self.get_coordinates()
        '''
        self.Edges = myE
        self.Verticies = myV
        '''
        
    def get_coordinates(self):
        coords = {}
        for i in self.Verticies:
            coords[i[0]] = (i[1],i[2])
        return coords
            
    
    def get_vert(self):
        return self.Verticies
    
    def get_neighbors(self):
        neighbors= defaultdict(list)
        for i in self.Verticies:
            for j in self.Edges:
                if j[0] == i[0]:
                    neighbors[(i[0])].append(j[1])
                if j[1] == i[0]:
                    neighbors[(i[0])].append(j[0])
        print(neighbors)
        return neighbors
    
    def find_vehicle(self, trucks):
        return random.choice(trucks)


    def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

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
        orderPaths = {}
        
        currentOrders = []
        
        for i in range(len(trucks)):
            vehicles[round((trucks[i].ID)/3)] = queue.Queue()
        
        for t in range(initialTime,finalTime):    
            print("\n\n Time: %02d:%02d"%(t/60, t%60))
            # each minute we can get a few new orders
            newOrders = self.getNewOrdersForGivenTime(t)
            num = len(newOrders) #get number of new orders
            # create lists to hold the starting and ending verticies of the orders
            
            for i in newOrders: #go through the new orders
                #set the starting and ending vertex (random)
                i.setStart(random.choice(self.Verticies)[0])
                i.setEnd(random.choice(self.Verticies)[0])
                i.setPath(self.graph) #create a path for the order
                currentOrders.append(i) #add the order to the list of current orders
            
            #vehicles[i].put(self.path(vehicle.currentPossition[1], startVerts))
            
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
            for k in self.coord: #for each vertex
                x = self.coord[k][0] #get x and y coordinates
                y = self.coord[k][1]
                #redraw the red rectangle
                pygame.draw.rect(self.screen, (255,0,0), 
                                 ((self.width*x/maxX)*self.scale, 
                                  (self.height*y/maxY)*self.scale, 10, 10))
            #go through all the order paths
            
            #DRAWING THE MOVING ORDERS AS WHITE
            for k in currentOrders: #go through current orders
                path = k.getPath() #get the path of the order
                if not path.empty(): #if the path isn't done
                    currentVertex = path.get() #get the first item in the path
                    x = self.coord[currentVertex][0] #get the coordinates of the current vertex
                    y = self.coord[currentVertex][1]
                    pygame.time.delay(100)
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
            for k in orderPaths:
                if orderPaths[k] != None: #if it isn't none
                    if not orderPaths[k].empty(): #if it isn't empty
                        currentVertex = orderPaths[k].get() #get the first item in the path
                        x = self.coord[currentVertex][0] #get the coordinates of the current vertex
                        y = self.coord[currentVertex][1]
                        pygame.time.delay(100)
                        if not orderPaths[k].qsize() == 0: #if we aren't at the last vertex
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
                    if orderPaths[k].empty(): #if the queue is empty
                        orderPaths[k] = None #set it as none so it isn't looked at next time

            '''
            self.screen.blit(text, textrect)
 
            
            '''
            You should plot the vetricies, edges and cars and customers
            Each time, cars will move and you should visualize it 
            accordingly
            '''
     
            pygame.display.update()    
            for event in pygame.event.get():
                pass   
            self.clock.tick(fps)
                
    
    def path(self, start, end):
        q = [[start]] #create a list that starts with just the start node
        visited = set() #create a set to hold the visited nodes
        
        while q: #while there are still lists in the queue
            path = q.pop(0) #path is the first element
            
            vertex = path[-1] #the vertex is the last point in the path
            
            if vertex == end: #if we are at the end
                print ("start: ", start)
                print ("end: ", end)
                print ("path: ", path)
                pathq = queue.Queue() #create a queue object to hold path
                pathq.queue = queue.deque(path) #convert list to queue object
                return pathq #return the queue
            elif vertex not in visited: #if the vertex hasn't been visited
                for neighbor in self.graph[vertex]: #go through the neighbors of the vertex
                    new_path= list(path) #make path into a list
                    new_path.append(neighbor) #add the neighbor to the new path
                    q.append(new_path) #put this path with a neighbor into the queue
            visited.add(vertex) #note that we visited the vertex
    