import math
from . import geometry
from .pod import Pod
from .geometry import Point, Convex
from .agent import Agent

class Tile(Agent):

    def __init__( self, identifier= 0, position= Point(0.0, 0.0), shape= None, matter=0):
        shape
        if shape is None :
            shape= Convex().initializeSquare(1.0)
        self._adjacencies= []
        self._agents= []
        super(Tile, self).__init__(identifier, 0, position, shape)
        self._matter= matter
        
    # Accessor:
    def adjacencies(self):
        return self._adjacencies

    def agents(self) :
        return self._agents
    
    def count(self) :
        return len( self._agents)
    
    def agent(self, i=1) :
        return self._agents[i-1]
    
    # Construction:
    def setAdjacencies( self, aList ):
        self._adjacencies= aList
        return self
    
    # Connection:
    def isConnecting(self, iTile):
        return (iTile in self.adjacencies())
    
    def connect(self, iTo):
        if iTo not in self._adjacencies :
            self._adjacencies.append(iTo)
            self._adjacencies.sort()
        return self

    def disconnect(self, iTo):
        self._adjacencies.remove(iTo)
        return self

    def connectAll( self, aList ):
        for iTo in aList :
            self.connect( iTo )
        return self
    
    def clockDirection( self, aPosition ):
        center= self.position()
        radius= self.radius()
        if center.distance( aPosition ) < radius :
            return 0
        clock= 1
        distance= aPosition.distance( center + geometry.clockPositions[1] )
        for i in range( 2, geometry.clockLenght ):
            option= center + geometry.clockPositions[i]
            d= aPosition.distance( option )
            if d < distance :
                clock= i
                distance= d
        return clock

    # Agent managment
    def append(self, aPod, brushId=0, shapeId=0 ): 
        self._agents.append( aPod )
        return self
    
    def clear(self):
        self._agents = []
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

    def bodyDistance(self, another):
        return self.body().distance( another.body() )

    # Pod interface:
    def asPod(self):
        return Pod().fromLists(   
            ["Tile"], 
            [self.id(), self.matter()] + self.adjacencies(),
            self.position().asList(),
            [self.shape().asPod()] + [ ag.asPod() for ag in self.agents() ]
        )
    
    def fromPod( self, aPod, agentFactory=Agent ):
        integers= aPod.integers()
        children= aPod.children()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setAdjacencies( integers[2:] )
        self.setPosition( Point().fromList( aPod.values() ) )
        self.setShape( Convex().fromPod( aPod.children()[0] ) )
        self.clear()
        for podBod in children[1:] :
            self.append( agentFactory().fromPod( podBod ) )
        return self
    
    # Classical Class
    def copy(self):
        cpy= type(self)()
        return cpy.fromPod( self.asPod() )
    
    # to str
    def str(self, typeName="Tile"): 
        # Myself :
        s= super(Tile, self).str(typeName)
        s+= " adjs"+ str(self._adjacencies)
        s+= f" agents({ len(self.agents()) })"
        return s
    
    def __str__(self): 
        return self.str()
    