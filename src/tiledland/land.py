from .tabletop import Tabletop
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
    def __init__( self, tabletop= None, bankOfEntities= [Entity()], bankOfAgents= [Agent()] ):
        self._bankOfEntities= bankOfEntities
        self._bankOfAgents= bankOfAgents
        if tabletop is None :
            tabletop= Tabletop()
        self.initTabletop(tabletop)
    
    def initializeDefaultBankOfEntities(self, bankOfEntitiesSize= 8, arrowtipSize= 0.8):
        names= ['X'] + [ chr( ord('A') + i%26 ) for i in range(bankOfEntitiesSize) ]
        self._bankOfEntities= [
            Entity( i, Convex().initArrowTip(arrowtipSize), name= names[i] )
            for i in range(bankOfEntitiesSize)
        ]
        return self

    def initializeArrowTipBankOfEntities(self, groups, arrowtipSizes, arrowtipAngles, names):
        self._bankOfEntities= [
            Entity( i+1, Convex().initArrowTip(s), orientation= a,  name= n )
            for i, s, a, n in zip( groups, arrowtipSizes, arrowtipAngles, names )
        ]
        return self

    # Accessor:
    def tabletop(self):
        return self._tabletop

    def size(self):
        return self._tabletop.size()

    def avatars(self):
        return self._avatars[1:]

    def agent(self, identifier):
        return self._avatars[identifier].agent()

    def agents(self):
        return [ a.agent() for a in self.avatars() ]

    def body(self, identifier):
        return self._avatars[identifier].body()

    def bodies(self):
        return [ a.body() for a in self.avatars() ]

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

    # Initializing:
    def initTabletop( self, tabletop ):
        self.clear()
        self._tabletop= tabletop
        return self

    # Construction:
    def clear( self ):
        self._avatars= [ Avatar(0, None, self) ]
    
    def appendAvatar(self, iTile, body, agent ):
        self._tabletop.tileAppendEntity( iTile, body )
        newId= len(self._avatars)
        body.setName( body.name() + "-" + str(newId) )
        self._avatars.append( Avatar(newId, body, agent) )
        return newId
    
    def popAvatar(self, iTile, entityNum=0, agentNum=0 ):
        return self.appendAvatar( iTile,
            self.bankEntity( entityNum ).copy(),
            self.bankAgent( agentNum ).copy() )
    
    def setBankOfAgents( self, aListOfAgents ):
        self._bankOfAgents= aListOfAgents
        return self

    def setBankOfEntities( self, aListOfEntities ):
        self._bankOfEntities= aListOfEntities
        return self

