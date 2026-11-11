from .map import CLOCK_ANGLE, Map
from .geometry import Convex
from .unit import Unit
from .agent import Agent

class Interface():
    def __init__(self, agent, unitSelectors=[]):
        assert type(unitSelectors) is list
        self._agent= agent
        self._unitSelectors= [(iTile, iUnit) for iTile, iUnit in unitSelectors]
    
    # accessor: 
    def agent(self):
        return self._agent

    def selectors(self):
        return self._unitSelectors

    def numberOfUnits(self):
        return len(self._unitSelectors)
    
    def selector(self, iUnit= 1):
        return self._unitSelectors[iUnit-1]

    def appendBody(self, body):
        self._unitSelectors.append(body)
        return len(self._unitSelectors)

    # Setters 
    def setSelector(self, iUnit, iTile, index):
        self._unitSelectors[iUnit-1]= (iTile, index)
        return self

class Land():
    def __init__( self, aMap= None ):
        if aMap is None :
            aMap= Map()
        self._map= aMap
        self._interfaces= [ Interface(self) ]

    # Accessor:
    def map(self):
        return self._map

    def size(self):
        return self._map.size()

    def interfaces(self):
        return self._interfaces

    def interface(self, iAgent):
        return self._interfaces[iAgent]

    def agent(self, identifier):
        return self.interface(identifier).agent()

    def agents(self):
        return [ itf.agent() for itf in self.interfaces() ]

    def selector(self, iAgent, iUnit=1):
        return self.interface(identifier).selector(iUnit)

    def allUnits(self):
        units= []
        for itf in self.interfaces() : 
            for iTile, iUnit in itf.selectors() : 
                units.append( self.map().unit(iTile, iUnit) )
        return units

    def agentUnit(self, iAgent, iUnit):
        iTile, index= self.interface(iAgent).selector(iUnit)
        return self.map().unit(iTile, index)

    # Map sortcut:
    def box(self):
        return self._map.box()

    def tile(self, iTile):
        return self._map.tile(iTile)

    # Construction:
    def appendAgent(self, agent, tileIds= [], units= [] ):
        if not type(tileIds) is list :
            tileIds= [tileIds]
            units= [units]
        iAgent= len(self._interfaces)
        selectors= []
        i= 1
        for iTile, body in zip( tileIds, units ) :
            body.setOwner(iAgent)
            body.setName( body.name() + f"-{i}" )
            index= self._map.tileAppendUnit( iTile, body )
            selectors.append( (iTile, index) )
            i+= 1
        self._interfaces.append( Interface(agent, selectors) )
        return iAgent

    def agentAddUnit(self, iAgent, iTile, unit):
        itf= self._interfaces[iAgent]
        iUnit= len(itf._unitSelectors)+1
        unit.setOwner(iAgent)
        unit.setName( unit.name() + f"-{iUnit}" )
        index= self._map.tileAppendUnit( iTile, unit )
        itf._unitSelectors.append( (iTile, index) )
        return (iTile, index)
    
    # Agent action execution :
    def actAgentMove(self, iAgent, iUnit, clockDir):
        iTile, index= self.interface(iAgent).selector(iUnit)
        body= self._map.unit(iTile, index)
        self._map.tileClockOrientUnit( iTile, index, clockDir )
        newTile, newIndex= self._map.tileClockMoveUnit( iTile, index, clockDir )
        self.interface(iAgent).setSelector(iUnit, newTile, newIndex)
        return (newTile, newIndex)

    def actAgentOrient(self, iAgent, iUnit, clockDir):
        iTile, index= self.interface(iAgent).selector(iUnit)
        body= self._map.unit(iTile, index)
        out= self._map.tileClockOrientUnit( iTile, index, clockDir )
        return out
    
    def actAgentRotateLeft(self, iAgent, iUnit, nbClockAngles= 1):
        iTile, index= self.interface(iAgent).selector(iUnit)
        body= self._map.unit(iTile, index)
        out= self._map.tileRotateUnitLeft( iTile, index, CLOCK_ANGLE*nbClockAngles )
        return out
    
    def actAgentRotateRight(self, iAgent, iUnit, nbClockAngles= 1):
        iTile, index= self.interface(iAgent).selector(iUnit)
        body= self._map.unit(iTile, index)
        out= self._map.tileRotateUnitLeft( iTile, index, -CLOCK_ANGLE*nbClockAngles )
        return out
    