import hacka
from .geometry import Point, Convex
from .entity import Entity

class Agent:
    def __init__(self, identifier=0):
        self._identifier= identifier
        self._map= None

    # Accessor:
    def id(self):
        return self._identifier
    
    def tile(self):
        return self._tile

    # Construction:    
    def setTile(self, aInteger):
        self._tile= aInteger
        return self
    
    
    # Agent Model:
    def perceive():
        return self
    
    def decide(self):
        return None
    
    # str:
    def str(self, typeName= "Agent"): 
        s= super().str(typeName)
        return s
    