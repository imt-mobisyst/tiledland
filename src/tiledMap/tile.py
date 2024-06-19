import math
from .point import Point2
from .segment import Segment


class Tile:

    # Initialization Destruction:
    def __init__( self, vertices= []):
        size= len(vertices)
        self._segments= []
        if vertices :
            self._segments= [
                Segment( v1, v2 )     
                for v1, v2 in zip( vertices, vertices[1:]+[vertices[0]] )
            ]
        self.updateCenter()

    # Construction:
    def updateCenter(self):
        self._center= Point2(0.0, 0.0)
        weights= 0.0
        for s in self.segments() :
            v= s.pointA() + s.pointB()
            dist= s.pointA().distance(s.pointB())
            v.scale(0.5)
            self._center.x+= v.x*dist
            self._center.y+= v.y*dist
            weights+= dist
        if weights > 0.0 :
            self._center.x/= weights
            self._center.y/= weights

    def add( self, aSegment ):
        self._segment.append( aSegment )
    
    def setTags( self, tags ):
        for s, t in zip( self.segments(), tags ) :
            s.setTag(t)
    
    # Accessors:
    def size(self):
        return len( self._segment )
    
    def center(self):
        return self._center
    
    def segments(self):
        return self._segments
