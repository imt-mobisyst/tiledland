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
    def __init__(self, aBody= None, aMap= None, state= None):
        self._body= aBody
        self._map= aMap
        if state is None :
            self.setStateProcessus(Agent.stateInitialize)
        else :
            self.setStateProcessus(state)

    def copy(self):
        b= None
        if self._body is not None :
            b= self._body.copy()
        m= None
        if self._map is not None :
            b= self._map.copy()
        cpy= type(self)( b, m, self._statePs )
        
        return cpy

    # Accessor:
    def perceivedBody(self):
        return self._map

    def perceivedMap(self):
        return self._map
    
    # Construction:

    # State Machine:
    def setStateProcessus(self, method):
        if hasattr(method, '__self__') :
            self._statePs= method.__func__
        else :
            self._statePs= method
        return self

    def runStateProcessus(self):
        return self._statePs(self)

    def stateInfinitWait(self):
        return Action(Action.WAIT)

    def stateInitialize(self):
        self.setStateProcessus( Agent.stateInfinitWait )
        return Action(Action.WAIT)

    # Agent Model:
    def perceive( self, body= None, map= None):
        return self
    
    def decide(self):
        action= self.runStateProcessus()
        return None
    
    
    # str:
    def str(self, typeName= "Agent"): 
        s= super().str(typeName)
        return s

class HackaAgent:
    pass