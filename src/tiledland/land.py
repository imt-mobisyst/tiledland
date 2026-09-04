from .tabletop import CLOCK_ANGLE, Tabletop
from .geometry import Convex
from .entity import Entity
from .agent import Agent

class Actor():
    def __init__(self, index, bodies, agent):
        assert type(bodies) is list
        self._id= index
        self._bodies= [b for b in bodies]
        self._agent= agent
    
    # accessor: 
    def agent(self):
        return self._agent

    def bodies(self):
        return self._bodies

    def numberOfBodies(self):
        return len(self._bodies)
    
    def body(self, iBody= 1):
        return self._bodies[iBody-1]

    def appendBody(self, body):
        self._bodies.append(body)
        return self

class Land():
    def __init__( self, tabletop= None, bankOfEntities= [Entity()] ):
        self._bankOfEntities= bankOfEntities
        if tabletop is None :
            tabletop= Tabletop()
        self.initTabletop(tabletop)
    
    # Initializing:
    def initTabletop( self, tabletop ):
        self.clear()
        self._tabletop= tabletop
        return self
    
    def initializeDefaultBankOfEntities(self, bankOfEntitiesSize= 8, arrowtipSize= 0.8):
        names= ['X'] + [ chr( ord('A') + i%26 ) for i in range(bankOfEntitiesSize) ]
        self._bankOfEntities= [
            Entity( i, Convex().initArrowTip(arrowtipSize), name= names[i] )
            for i in range(bankOfEntitiesSize)
        ]
        return self

    def initializeArrowTipBankOfEntities(self, groups, arrowtipSizes, arrowtipAngles, names):
        self._bankOfEntities= [
            Entity( i, Convex().initArrowTip(s), orientation= a,  name= n )
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

    def body(self, identifier, iBody=1):
        return self._actors[identifier].body(iBody)

    def allBodies(self):
        bodies= []
        for a in self.actors() : 
            bodies+= a.bodies()
        return bodies

    def bankOfEntities( self ):
        return self._bankOfEntities

    def bankEntity( self, num=0 ):
        i= num%(len(self._bankOfEntities))
        return self._bankOfEntities[i]


    # Tabletop sortcut:
    def tile(self, iTile):
        return self._tabletop.tile(iTile)

    # Construction:
    def clear( self ):
        self._actors= [ Actor(0, [], self) ]
    
    def appendActor(self, agent, tileIds= [], bodyIds= [] ):
        newId= len(self._actors)
        bodies= []
        i= 1
        for bi, t in zip(bodyIds, tileIds ) :
            body= self.bankEntity( bi ).copy()
            body.setName( body.name() + f"-{i}" )
            self._tabletop.tileAppendEntity( t, body )
            bodies.append(body)
            i+= 1
        self._actors.append( Actor(newId, bodies, agent) )
        return newId

    def popActorBody(self, iActor, iTile, entityNum= -1):
            a= self.actor(iActor)
            nextId= a.numberOfBodies()+1
            if entityNum < 0 :
                entityNum= iActor
            body= self.bankEntity( entityNum ).copy()
            body.setName( body.name() + "-" + str(nextId) )
            self._tabletop.tileAppendEntity( iTile, body )
            a.appendBody(body)
            return body

    def popSimpleActor(self, agent, iTile ):
        entityNum= len(self._actors)
        return self.appendActor( agent, [iTile], [entityNum] )

    def setBankOfEntities( self, aListOfEntities ):
        self._bankOfEntities= aListOfEntities
        return self

    # Actor action :
    def actBodyMove(self, iActor, iBody, clockDir):
        body= self.actor(iActor).body(iBody)
        self._tabletop.tileClockOrientEntity( body.location(), body.index(), clockDir )
        newlocation= self._tabletop.tileClockMoveEntity( body.location(), body.index(), clockDir )
        return newlocation

    def actBodyOrient(self, iActor, iBody, clockDir):
        body= self.actor(iActor).body(iBody)
        out= self._tabletop.tileClockOrientEntity( body.location(), body.index(), clockDir )
        return out
    
    def actBodyRotateLeft(self, iActor, iBody, nbClockAngles= 1):
        iTile, index= self.actor(iActor).body(iBody).selector()
        out= self._tabletop.tileRotateEntityLeft( iTile, index, CLOCK_ANGLE*nbClockAngles )
        return out
    
    def actBodyRotateRight(self, iActor, iBody, nbClockAngles= 1):
        iTile, index= self.actor(iActor).body(iBody).selector()
        out= self._tabletop.tileRotateEntityLeft( iTile, index, -CLOCK_ANGLE*nbClockAngles )
        return out
    