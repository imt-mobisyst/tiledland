import math, shapely
from .geometry import Coord2, Segment

class Joint:
    # Initialization Destruction:
    def __init__( self, tileA= None, tileB= None, gateA= 0, gateB= 0 ):
        self._tileA= tileA
        self._gateA= gateA
        self._tileB= tileB
        self._gateB= gateB
        self._tag= 0
    
    # Accessors:
    def tileA(self):
        return  self._tileA
    
    def tileB(self):
        return self._tileB

    def updateGates( self ):
        self._gateA= self.tileA().findGateSegment( self.tileB().center() )
        self._gateB= self.tileB().findGateSegment( self.tileA().center() )
        return ( type(self._gateA) == int and type(self._gateB) == int )

    def gates(self):
        return (
            self.tileA().segment( self._gateA ),
            self.tileB().segment( self._gateB )
        )

    def shapeSegments(self):
        a1, a2= self.tileA().segment( self._gateA ).tuple()
        b1, b2= self.tileB().segment( self._gateB ).tuple()
        return [
            Segment(a1, a2),
            Segment(a2, b1),
            Segment(b1, b2),
            Segment(b2, a1)
        ]

    def frontiere(self):
        a1, a2= self.tileA().segment( self._gateA ).tuple()
        xa1, ya1= a1.tuple()
        xa2, ya2= a2.tuple()
        b1, b2= self.tileB().segment( self._gateB ).tuple()
        xb1, yb1= b1.tuple()
        xb2, yb2= b2.tuple()
        return Segment(
            Coord2((xa1+xb2)/2, (ya1+yb2)/2),
            Coord2((xb1+xa2)/2, (yb1+ya2)/2)
        )
    
    # Construction: