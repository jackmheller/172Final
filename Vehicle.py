from Classes.AbstractVehicle import AbstractVehicle
from random import random

class Vehicle(AbstractVehicle):
    vehicles = []
    
    def __init__(self, ID, v):
        AbstractVehicle.__init__(self,ID,v)
        busy = False
        self.vehicles.append(ID)