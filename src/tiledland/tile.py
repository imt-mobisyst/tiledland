import math, hacka
from . import geometry, artist
from .geometry import Point, Convex
from .entity import Entity, Entity

_defaultOutline= Convex().initSquare(1.0)

class Tile(Entity):
    # Initialization / Destruction:
    def __init__(self,
                    outline= _defaultOutline, position=Point(), angle=0.0,
                    color0x=0x000000, enclave=0, index=0 ):
        self._adjacencies= []
        self._entities= []
        self._size= 0
        super(Tile, self).__init__(outline, position, angle, color0x, enclave, index)
    
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
        cpy._entities= [ent for ent in self._entities]
        self._size= len(cpy._entities)

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
        self._entities.append( anEntity )
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
        ent= self._entities.pop(i)
        self._size= len(self._entities)
        for j in range( i, self._size ) :
            self._entities[j].setIndex(j+1)
        return ent
    
    def clear(self):
        self._entities = []
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
        s+= f" entities({ len(self.entities()) })"
        return s
    
    def __str__(self): 
        return self.str()

