from  AbstractWorld import AbstractWorld

import pygame
pygame.font.init() 

class World(AbstractWorld):
    
    def __init__(self):
        AbstractWorld.__init__(self)
        
        self.height = 600
        self.width = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.black = (0,0,0)
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont('Comic Sans MS', 30)


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
        for t in xrange(initialTime,finalTime):    
            print("\n\n Time: %02d:%02d"%(t/60, t%60))
            # each minute we can get a few new orders
            newOrders = self.getNewOrdersForGivenTime(t)
            print("New orders:")
            for c in newOrders:
                print(c)
            
            text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
            textrect = text.get_rect()
            textrect.centerx = 100
            textrect.centery = 30
            self.screen.fill((255, 255, 255))
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
        