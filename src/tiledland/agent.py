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
    def __init__(self, aBody= None, tabletop= None, state= None):
        self._body= aBody
        self._tabletop= tabletop
        if state is None :
            self.setStateProcessus(Agent.stateInitialize)
        else :
            self.setStateProcessus(state)

    def copy(self):
        b= None
        if self._body is not None :
            b= self._body.copy()
        m= None
        if self._tabletop is not None :
            b= self._tabletop.copy()
        cpy= type(self)( b, m, self._statePs )
        
        return cpy

    # Accessor:
    def perceivedBody(self):
        return self._tabletop

    def perceivedTabletop(self):
        return self._tabletop
    
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
    def perceive( self, body= None, tabletop= None):
        return self
    
    def decide(self):
        action= self.runStateProcessus()
        return None
    
    # str:
    def str(self, typeName= "Agent"): 
        s= typeName
        return s

    def __str__(self):
        return self.str()
    
class HackaAgent:
    pass