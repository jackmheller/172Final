from Classes.AbstractWorld import AbstractWorld
import random
import pygame
import numpy as np
from networkx.classes.function import neighbors
import queue
import math
pygame.font.init() 

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
        
    def get_vert(self):
        return self.Verticies
    
    def get_neighbors(self):
        neighbors= {}
        for i in self.Verticies:
            for j in self.Edges:
                if j[0] == i:
                    neighbors[i].append(j[1])
                if j[1] == i:
                    neighbors[i].append(j[2])
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
        for i in range(len(trucks)):
            vehicles[round((trucks[i].ID)/3)] = queue.Queue()
        for t in range(initialTime,finalTime):    
            print("\n\n Time: %02d:%02d"%(t/60, t%60))
            # each minute we can get a few new orders
            newOrders = self.getNewOrdersForGivenTime(t)
            num = len(newOrders)
            startVerts = []
            endVerts = []
            vehicle = self.find_vehicle(trucks)
            for i in range(num):
                startVerts.append(random.choice(self.Verticies))
                endVerts.append(random.choice(self.Verticies))
            vehicles[i].put(self.path(vehicle.currentPossition[1], startVerts))
            for j in range(len(startVerts)):
                start = startVerts[j]
                end = endVerts[j]
                vehicles[i].put(self.path(start[0], end[0]))
            print("New orders:")
            for c in newOrders:
                print(c)
            
            text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
            textrect = text.get_rect()
            textrect.centerx = 100
            textrect.centery = 30
            #self.screen.fill((255, 255, 255))
            
            for k in range(len(vehicles)):
                vert = vehicles.get(queue)
                if vert != None:
                    x = self.Verticies[vert][1]
                    y = self.Verticies[vert][2]
                    pygame.draw.rect(self.screen, (255,255,255), 
                                     ((self.width*x/maxX)*self.scale, 
                                      (self.height*y/maxY)*self.scale, 10, 10))
                    
                
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
        graph = self.get_neighbors()
        # maintain a queue of paths
        queue = []
        # push the first path into the queue
        queue.append([start])
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1]
            # path found
            if node == end:
                return path
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for n in graph.get(node, []):
                new_path = list(path)
                new_path.append(n)
                queue.append(new_path)
    
            
            
            
            
