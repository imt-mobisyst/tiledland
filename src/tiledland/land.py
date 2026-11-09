from .map import CLOCK_ANGLE, Map
from .geometry import Convex
from .unit import Unit
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
    def __init__( self, aMap= None, bankOfUnits= [] ):
        self._bankOfUnits= [model for model in bankOfUnits]
        if len(self._bankOfUnits) == 0 :
            self._bankOfUnits= [ Unit() ]
        if aMap is None :
            aMap= Map()
        self.initMap(aMap)
    
    # Initializing:
    def clear( self ):
        self._actors= [ Actor(0, [], self) ]
    
    def initMap( self, aMap ):
        self.clear()
        self._map= aMap
        return self
    
    def initializeDefaultBankOfUnits(self, bankOfUnitsSize= 8, arrowtipSize= 0.8):
        names= ['X'] + [ chr( ord('A') + i%26 ) for i in range(bankOfUnitsSize) ]
        self._bankOfUnits= [
            Unit( Convex().initArrowTip(arrowtipSize), owner= i, name= names[i] )
            for i in range(bankOfUnitsSize)
        ]
        return self

    def initializeArrowTipBankOfUnits(self, groups, arrowtipSizes, arrowtipAngles, names):
        self._bankOfUnits= [
            Unit( Convex().initArrowTip(s), orientation= a, owner= i, name= n )
            for i, s, a, n in zip( groups, arrowtipSizes, arrowtipAngles, names )
        ]
        return self

    # Accessor:
    def map(self):
        return self._map

    def size(self):
        return self._map.size()

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

    def bankOfUnits( self ):
        return self._bankOfUnits

    def bankUnit( self, num=0 ):
        i= num%(len(self._bankOfUnits))
        return self._bankOfUnits[i]


    # Map sortcut:
    def box(self):
        return self._map.box()

    def tile(self, iTile):
        return self._map.tile(iTile)

    # Construction:
    def appendActor(self, agent, tileIds= [], bodyIds= [] ):
        newId= len(self._actors)
        bodies= []
        i= 1
        for bi, t in zip(bodyIds, tileIds ) :
            body= self.bankUnit( bi ).copy()
            body.setName( body.name() + f"-{i}" )
            self._map.tileAppendUnit( t, body )
            bodies.append(body)
            i+= 1
        self._actors.append( Actor(newId, bodies, agent) )
        return newId

    def popActorBody(self, iActor, iTile, entityNum= -1):
            a= self.actor(iActor)
            nextId= a.numberOfBodies()+1
            if entityNum < 0 :
                entityNum= iActor
            body= self.bankUnit( entityNum ).copy()
            body.setName( body.name() + "-" + str(nextId) )
            self._map.tileAppendUnit( iTile, body )
            a.appendBody(body)
            return body

    def popSimpleActor(self, agent, iTile ):
        entityNum= len(self._actors)
        return self.appendActor( agent, [iTile], [entityNum] )

    def setBankOfUnits( self, aListOfUnits ):
        self._bankOfUnits= aListOfUnits
        return self

    # Actor action :
    def actBodyMove(self, iActor, iBody, clockDir):
        body= self.actor(iActor).body(iBody)
        self._map.tileClockOrientUnit( body.enclave(), body.index(), clockDir )
        newlocation= self._map.tileClockMoveUnit( body.enclave(), body.index(), clockDir )
        return newlocation

    def actBodyOrient(self, iActor, iBody, clockDir):
        body= self.actor(iActor).body(iBody)
        out= self._map.tileClockOrientUnit( body.enclave(), body.index(), clockDir )
        return out
    
    def actBodyRotateLeft(self, iActor, iBody, nbClockAngles= 1):
        iTile, index= self.actor(iActor).body(iBody).selector()
        out= self._map.tileRotateUnitLeft( iTile, index, CLOCK_ANGLE*nbClockAngles )
        return out
    
    def actBodyRotateRight(self, iActor, iBody, nbClockAngles= 1):
        iTile, index= self.actor(iActor).body(iBody).selector()
        out= self._map.tileRotateUnitLeft( iTile, index, -CLOCK_ANGLE*nbClockAngles )
        return out
    