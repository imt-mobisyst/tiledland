import math, shapely
from .geometry import Coord2, Segment

class Joint:
    # Initialization Destruction:
    def __init__( self, tileA= None, tileB= None, segmentA= 0, segmentB= 0 ):
        self._tileA= tileA
        self._segmentA= segmentA
        self._tileB= tileB
        self._segmentB= segmentB
        self._tag= 0
    
    # Accessors:
    def tileA(self):
        return  self._tileA
    
    def tileB(self):
        return self._tileB

    def updateSegments( self ):
        self._segmentA= self.tileA().findExitSegment( self.tileB().center() )
        self._segmentB= self.tileB().findExitSegment( self.tileA().center() )
        return ( type(self._segmentA) == int and type(self._segmentB) == int )

    def segments(self):
        return [
            self.tileA().segment( self._segmentA ),
            self.tileB().segment( self._segmentB )
        ]

    def shapeSegments(self):
        a1, a2= self.tileA().segment( self._segmentA ).tuple()
        b1, b2= self.tileB().segment( self._segmentB ).tuple()
        return [
            Segment(a1, a2),
            Segment(a2, b1),
            Segment(b1, b2),
            Segment(b2, a1)
        ]

    def frontiere(self):
        a1, a2= self.tileA().segment( self._segmentA ).tuple()
        xa1, ya1= a1.tuple()
        xa2, ya2= a2.tuple()
        b1, b2= self.tileB().segment( self._segmentB ).tuple()
        xb1, yb1= b1.tuple()
        xb2, yb2= b2.tuple()
        return Segment(
            Coord2((xa1+xb2)/2, (ya1+yb2)/2),
            Coord2((xb1+xa2)/2, (yb1+ya2)/2)
        )
    
    # Construction: