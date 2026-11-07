import math, hacka
from . import geometry, artist
from .geometry import Point, Convex
from .shaped import AbsShaped, Shaped

def _defaultShape():
    return Convex().initSquare(1.0)

class Tile(Shaped):
    # Initialization / Destruction:
    def __init__(self, shape= _defaultShape(),
            owner=0, category=0, index=0, name="Tile"):
        super().__init__(shape, owner, category, index, name)
        assert type(shape) == Convex
        self._adjacencies= []
        self._units= []
        self._size= 0
    
    def copy(self):
        cpy= type(self)(
            self._group,
            self._refShape,
            self._position, self._theta,
            self._brush,
            self._local, self._index,
            self._name
        )
        cpy._adjacencies= [nei for nei in self._adjacencies]
        cpy._units= [ent for ent in self._units]
        self._size= len(cpy._units)

    # Accessor:
    def adjacencies(self):
        return self._adjacencies

    def units(self):
        return self._units
    
    def numberOfEntities(self):
        return self._size

    def unit(self, i=1) :
        return self._units[i-1]
    
    # Construction:
    def setIndex(self, index):
        for e in self.units() :
            e.setEnclave(index)
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
        self._units.append( anEntity )
        self._size+= 1
        anEntity.setSelector( self._index, self._size )
        return self

    def appendCenter(self, anEntity ):
        self.append( anEntity )
        anEntity.setPose( self.position(), anEntity.orientation() )
        anEntity.setIndex( self.numberOfEntities() )
        return anEntity
    
    def remove(self, iEntity):
        i= iEntity-1
        ent= self._units.pop(i)
        self._size= len(self._units)
        for j in range( i, self._size ) :
            self._units[j].setIndex(j+1)
        return ent
    
    def clear(self):
        self._units = []
        self._size= 0
        return self
    
    # Artist drawing:
    def renderOn(self, artist):
        artist.drawConvex( self.shape(), self.brush() )
        return self

    def writeOn(self, artist, text):
        if text == "" :
            return self
        minx, miny= self.box().leftFloor().asTuple()
        x, y= self.position().asTuple()
        x= x+(minx-x)*2/3
        y= y+(miny-y)*2/3
        artist.write( x, y, text, self.brush() )
        return self
    
    # to String
    def str(self): 
        # Myself :
        s= super(Tile, self).str()
        s+= " adjs"+ str(self._adjacencies)
        s+= f" entities({ len(self.units()) })"
        return s
    
    def __str__(self): 
        return self.str()

