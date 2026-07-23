import hacka
from .geometry import Point, Convex
from .entity import Entity

class Action:
    WAIT= 0
    MOVE= 1

    def __init__(self, actionIdentifier= 0, attributes= []):
        self._id= actionIdentifier
        self._attributes= [x for x in attributes]
    
    # Accessor:
    def identifier(self):
        return self._id

    def attributes(self):
        return self._attributes
    
    # Construction:    

class Agent:
    def __init__(self):
        self._body= None
        self._map= None
        self._statePs= self.stateInfinitWait

    # Accessor:
    def perceivedBody(self):
        return self._map

    def perceivedMap(self):
        return self._map
    
    # Construction:    
    def setStateProcessus(self, method):
        self._statePs= method
        return self

    # Agent Model:
    def perceive( self, body= None, map= None):
        return self
    
    def decide(self):
        action= self.stateProcess()()
        return None
    
    # State Machine:
    def runStateProcessus(self):
        return self._statePs()
    
    def stateInfinitWait(self):
        return Action(Action.WAIT)

    # str:
    def str(self, typeName= "Agent"): 
        s= super().str(typeName)
        return s

class HackaAgent:
    pass