import math, hacka
from . import geometry
from .geometry import Point, Convex
from .entity import Entity
from .artist import palette

class Tile(Entity):
    defaultShape= Convex().initSquare(1.0)
    defaultPalette= palette.background

    def __init__( self, identifier= 0, group=0, shape= None, position= Point(0.0, 0.0), orientation= 0.0):
        super(Tile, self).__init__( group, shape, position, orientation, None, 0, identifier, "Tile")
        self._adjacencies= []
        self._entities= []
        self._size= 0
        
    # Accessor:
    def adjacencies(self):
        return self._adjacencies

    def entities(self):
        return self._entities
    
    def numberOfEntities(self):
        return self._size

    def entity(self, i=1) :
        return self._entities[i-1]
    
    # Construction:
    def setIndex(self, index):
        for e in self.entities() :
            e.setArea(index)
        self._index= index
        return self
    
    def setAdjacencies( self, aList ):
        self._adjacencies= aList
        return self
    
    # Connection:
    def isConnecting(self, iTile):
        return (iTile in self.adjacencies())
    
    def connect(self, iTo):
        assert( type(iTo) == int )
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

    # Entity managment
    def append(self, anEntity ): 
        self._entities.append( anEntity )
        self._size+= 1
        anEntity.setLocation( self._index, self._size )
        return self

    def appendCenter(self, anEntity ):
        self.append( anEntity )
        anEntity.setPose( self.position(), anEntity.orientation() )
        anEntity.setIndex( self.numberOfEntities() )
        return anEntity
    
    def remove(self, iEntity):
        i= iEntity-1
        ent= self._entities.pop(i)
        self._size= len(self._entities)
        for j in range( i, self._size ) :
            self._entities[j].setIndex(j+1)
        return ent
    
    def clear(self):
        self._entities = []
        self._size= 0
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

    def bodyDistance(self, another):
        return self.projectedShape().distance( another.projectedShape() )

    # hacka.DataTree Interface:
    def asDataTree(self):
        x, y = self.position().asTuple()
        return hacka.DataTree("Tile", 
            [self.index(), self.group()] + self.adjacencies(),
            [x, y, self.orientation()],
            [self.referenceShape().asDataTree()] + [ ag.asDataTree() for ag in self.entities() ]
        )
    
    def fromDataTree( self, aDataTree, entityClass=Entity ):
        digits= aDataTree.digits()
        values= aDataTree.values()
        children= aDataTree.children()
        self.setIndex( digits[0] )
        self.setGroupAndBrush( digits[1] )
        self.setAdjacencies( digits[2:] )
        self.referenceShape().fromDataTree( children[0] )
        self.setPose( Point(values[0], values[1]), values[2] )
        self.clear()
        for c in children[1:] :
            ent= entityClass().fromDataTree( c )
            self.append( ent )
        return self
    
    # Classical Class
    def copy(self):
        cpy= type(self)()
        return cpy.fromDataTree( self.asDataTree() )
    
    # Artist drawing:
    def renderOn(self, artist):
        artist.drawConvex( self.projectedShape(), self.brush() )

    def writeOn(self, artist):
        minx, miny= self.box().leftFloor().asTuple()
        x, y= self.position().asTuple()
        x= x+(minx-x)*2/3
        y= y+(miny-y)*2/3
        artist.write( x, y, str(self.index()), self.brush() )

    # to str
    def str(self): 
        # Myself :
        s= super(Tile, self).str()
        s+= " adjs"+ str(self._adjacencies)
        s+= f" entities({ len(self.entities()) })"
        return s
    
    def __str__(self): 
        return self.str()
    