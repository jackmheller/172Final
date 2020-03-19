from Classes.AbstractVehicle import AbstractVehicle
from random import random

class Vehicle(AbstractVehicle):
    vehicles = []
    
    def __init__(self, ID, v, busy):
        AbstractVehicle.__init__(self,ID,v)
        busy = False
        self.vehicles.append(ID)

    def find_vehicle(self):
        veh = random.choice(self.vehicles)
        if veh.busy == True:
            self.find_vehicle()
        return veh