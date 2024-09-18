import math, shapely
from typing import Any
from .geometry import Coord2, Segment

class Tile:

    # Initialization Destruction:
    def __init__( self, center= Coord2(), id= 0, tag= 0):
        self._center= center
        self._id= 0
        self._tag= tag
        self._limitCoords= []
        self._limitTags= []

    # Deep Copy:
    def copy(self):
        deep= Tile( self._center, self._id, self._tag )
        deep._limitCoords= [ coord.copy() for coord in self._limitCoords ]
        deep._limitTags= [ tag for tag in self._limitTags ]
        return deep

    def setSegementTags( self, tags ):
        assert( len(tags) == self.size() )
        self._limitTags= tags
        return self
    
    def setTag( self, tag ):
        self._tag= tag
        return self
    
    # Construction:
    def setId(self, i):
        self._id= i
        return self
    
    def setFromCoordinates( self, coords ):
        self._limitCoords= list(coords)
        self.updateCenter()
        self._limitTags= [ self.tag() for c in self._limitCoords ]
        return self

    def setFromList( self, l ):
        return self.setFromCoordinates([
            Coord2().setFromTuple( t )
            for t in l
        ])

    def setSquare(self, center, lenght):
        demi= lenght*0.5
        self._limitCoords= [
            Coord2( center._x-demi, center._y+demi ),
            Coord2( center._x+demi, center._y+demi ),
            Coord2( center._x+demi, center._y-demi ),
            Coord2( center._x-demi, center._y-demi )
        ]
        self._limitTags= [ self.tag() for i in range(4) ]
        self._center= center
        return self

    def setRegular(self, numberOfVertex, center, size):
        radius= size*0.5
        x, y= center.tuple()
        self._limitCoords= []
        self._limitTags= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            self._limitCoords.append( Coord2(
                x+math.cos(angle)*radius,
                y+math.sin(angle)*radius
            ) )
            angle+= -delta
            self._limitTags.append( self.tag() )
        self._center= center
        return self
    


    # Updates:
    def updateCenter(self):
        shape= shapely.Polygon( [ c.tuple() for c in self._limitCoords ] )
        center= shapely.centroid(shape)
        self._center= Coord2(center.x, center.y)
        return self

    # Accessors:
    def center(self):
        return self._center
    
    def id(self):
        return self._id
    
    def tag(self):
        return self._tag
    
    def size(self):
        return len(self._limitCoords)
    
    def limit(self):
        return self._limitCoords

    def segmentACoords(self):
        return self._limitCoords
    
    def segmentBCoords(self):
        return self._limitCoords[1:] + [ self._limitCoords[0] ]
    
    def segments(self):
        if self.size() <= 1:
            return []
        return [
            Segment( a, b )
            for a, b in zip( self.segmentACoords(), self.segmentBCoords() )
        ]
    
    def segment(self, i):
        return Segment( self.segmentACoords()[i], self.segmentBCoords()[i] )
    
    def segmentTags(self):
        return self._limitTags

    def findGateSegment( self, aTargetCoordinate ):
        lineOut= shapely.LineString( [self.center().tuple(), aTargetCoordinate.tuple()] )
        segmentList= self.segments()
        iSegment= 0
        for segment in segmentList :
            inter= shapely.get_coordinates( 
                shapely.intersection( lineOut, shapely.LineString( segment.list() ) )
            )
            if len(inter) > 0 :
                return iSegment
            iSegment+= 1
        return False
    
    # Modifier:
    def move( self, transform ):
        self._limitCoords= [ coord+transform for coord in self._limitCoords ]
        self._center= self._center + transform
        return self
    
    def moveTo( self, aCoordinate ):
        transform= aCoordinate - self._center
        return self.move( transform )