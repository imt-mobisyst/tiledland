from .map import Map
from .geometry import Convex
from .entity import Entity
from .agent import Agent

class Avatar():
    def __init__(self, index, body, agent):
        self._id= index
        self._body= body
        self._agent= agent
    
    # accessor: 
    def agent(self):
        return self._agent

    def body(self):
        return self._body

class Land():
    def __init__( self, aMap= None, bankOfEntitiesSize= 8, bankOfAgentsSize= 4 ):
        self._map= aMap
        if self._map is None :
            self._map= Map()
        self._avatars= [ Avatar(0, None, None) ]
        self._bankOfEntities= [
            Entity( i, Convex().initArrowTip(0.8), name= chr( ord('A') + i%26 ) )
            for i in range(bankOfEntitiesSize)
        ]
        self._bankOfAgents= [Agent() for _ in range(bankOfAgentsSize)]

    # Accessor:
    def map(self):
        return self._map

    def agent(self, identifier):
        return self._avatars[identifier].agent()

    def body(self, identifier):
        return self._avatars[identifier].body()
    
    def bankOfEntities( self ):
        return self._bankOfEntities

    def bankEntity( self, num=0 ):
        i= num%(len(self._bankOfEntities))
        return self._bankOfEntities[i]

    def bankOfAgents( self ):
        return self._bankOfAgents
    
    def bankAgent( self, num=0 ):
        i= num%(len(self._bankOfAgents))
        return self._bankOfAgents[i]

    # Construction:
    def appendAvatar(self, iTile, body, agent ):
        newId= len(self._avatars)
        self._map.tileAppendEntity( iTile, body )
        self._avatars.append( Avatar(newId, body, agent) )
        return newId
    
    def popAvatar(self, iTile, entityNum=0, agentNum=0 ):
        return self.appendAvatar( iTile,
            self.bankEntity( entityNum ).copy(),
            self.bankAgent( agentNum ).copy()
        )
    
    def setBankOfAgents( self, aListOfAgents ):
        self._bankOfAgents= aListOfAgents
        return self

    def setBankOfEntities( self, aListOfEntities ):
        self._bankOfEntities= aListOfEntities
        return self

