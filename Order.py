from Classes.Vehicle import Vehicle
from Classes.AbstractOrder import AbstractOrder
from random import random
import numpy as np


class Order(AbstractOrder):
    
    def __init__(self, id):
        AbstractOrder.__init__(self, id)
        

