import math, hacka
from . import geometry
from .geometry import Point, Convex
from .entity import Entity
from .agent import Agent
from .artist import palette

class Tile(Entity):

    def __init__( self, identifier= 0, group=0, shape= None, position= Point(0.0, 0.0), orientation= 0.0):
        if shape is None :
            shape= Convex().initSquare(1.0)
        super(Tile, self).__init__(identifier, group, shape)
        self.setPose( position, orientation )
        self._adjacencies= []
        self._agents= []
        
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
    
    # Artist :
    def setGroupAndBrush(self, aGroupId):
        iBrush= aGroupId%len(palette.foreground)
        self._brush= palette.background[iBrush]
        self._group= aGroupId
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
    def append(self, aDataTree, brushId=0, shapeId=0 ): 
        self._agents.append( aDataTree )
        return self
    
    def clear(self):
        self._agents = []
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

    def bodyDistance(self, another):
        return self.body().distance( another.body() )

    # hacka.DataTree Interface:
    def asDataTree(self):
        x, y = self.position().asTuple()
        return hacka.DataTree("Tile", 
            [self.id(), self.group()] + self.adjacencies(),
            [x, y, self.orientation()],
            [self.referenceShape().asDataTree()] + [ ag.asDataTree() for ag in self.agents() ]
        )
    
    def fromDataTree( self, aDataTree, agentFactory=Agent ):
        digits= aDataTree.digits()
        values= aDataTree.values()
        children= aDataTree.children()
        self.setId( digits[0] )
        self.setGroupAndBrush( digits[1] )
        self.setAdjacencies( digits[2:] )
        self.referenceShape().fromDataTree( children[0] )
        self.setPose( Point(values[0], values[1]), values[2] )
        self.clear()
        for c in children[1:] :
            self.append( agentFactory().fromDataTree( c ) )
        return self
    
    # Classical Class
    def copy(self):
        cpy= type(self)()
        return cpy.fromDataTree( self.asDataTree() )
    
    # Artist drawing:
    def renderOn(self, artist):
        artist.drawConvex( self.body(), self.brush() )

    def writeOn(self, artist):
        minx, miny= self.box().leftFloor().asTuple()
        x, y= self.position().asTuple()
        x= x+(minx-x)*2/3
        y= y+(miny-y)*2/3
        artist.write( x, y, str(self.id()), self.brush() )

    # to str
    def str(self, typeName): 
        # Myself :
        s= super(Tile, self).str(typeName)
        s+= " adjs"+ str(self._adjacencies)
        s+= f" agents({ len(self.agents()) })"
        return s
    
    def __str__(self): 
        return self.str("Tile")
    