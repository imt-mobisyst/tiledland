import math, shapely
from typing import Any
from .geometry import Coord2, Segment

class Tile:

    # Initialization Destruction:
    def __init__( self, center= Coord2() ):
        self._center= center
        self._limitCoords= []
        self._tags= []

    def setTags( self, tags ):
        assert( len(tags) == self.size() )
        self._tags= tags
        return self
    
    # Construction:
    def setFromCoordinates( self, coords ):
        self._limitCoords= list(coords)
        self.updateCenter()
        self._tags= [ 0 for c in self._limitCoords ]
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
        self._tags= [0, 0, 0, 0]
        self._center= center
        return self

    def setRegular(self, numberOfVertex, center, size):
        radius= size*0.5
        x, y= center.tuple()
        self._limitCoords= []
        self._tags= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            self._limitCoords.append( Coord2(
                x+math.cos(angle)*radius,
                y+math.sin(angle)*radius
            ) )
            angle+= -delta
            self._tags.append( 0 )
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
        return self._tags

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