from .tabletop import Tabletop
from .geometry import Convex
from .entity import Entity
from .agent import Agent

class Actor():
    def __init__(self, index, bodies, agent):
        assert type(bodies) is list
        self._id= index
        self._bodies= bodies
        self._agent= agent
    
    # accessor: 
    def agent(self):
        return self._agent

    def bodies(self):
        return self._bodies
    
    def appendBody(self, body):
        self._bodies.append(body)
        return self


class Land():
    def __init__( self, tabletop= None, bankOfEntities= [Entity()] ):
        self._bankOfEntities= bankOfEntities
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

    def actors(self):
        return self._actors

    def actor(self, iActor):
        return self._actors[iActor]

    def agent(self, identifier):
        return self._actors[identifier].agent()

    def agents(self):
        return [ a.agent() for a in self.actors() ]

    def body(self, identifier):
        return self._actors[identifier].body()

    def bodies(self):
        return [ a.body() for a in self.actors() ]

    def bankOfEntities( self ):
        return self._bankOfEntities

    def bankEntity( self, num=0 ):
        i= num%(len(self._bankOfEntities))
        return self._bankOfEntities[i]

    # Initializing:
    def initTabletop( self, tabletop ):
        self.clear()
        self._tabletop= tabletop
        return self

    # Construction:
    def clear( self ):
        self._actors= [ Actor(0, [], self) ]
    
    def appendActor(self, agent, tileIds= [], bodies= [] ):
        newId= len(self._actors)
        for b, t in zip(bodies, tileIds ) :
            self._tabletop.tileAppendEntity( t, b )
            b.setName( b.name() + "-" + str(newId) )
        self._actors.append( Actor(newId, bodies, agent) )
        return newId
        
    def popActorBody(self, iActor, iTile, entityNum):
            body= self.bankEntity( entityNum ).copy()
            body.setName( body.name() + "-" + str(iActor) )
            self._tabletop.tileAppendEntity( iTile, body )
            self.actor(iActor).appendBody(body)
            return self
    
    def popSimpleActor(self, agent, iTile, entityNum ):
        return self.appendActor( agent, [iTile], [self.bankEntity( entityNum ).copy()] )

    def setBankOfEntities( self, aListOfEntities ):
        self._bankOfEntities= aListOfEntities
        return self

