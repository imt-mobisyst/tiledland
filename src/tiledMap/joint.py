import math, shapely

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
        a1, a2= self.tileA().segment( self._segmentA )
        b1, b2= self.tileB().segment( self._segmentB )
        return [
            (a1, a2),
            (a2, b1),
            (b1, b2),
            (b2, a1)
        ]

    def frontiere(self):
        a1, a2= self.tileA().segment( self._segmentA )
        xa1, ya1= a1
        xa2, ya2= a2
        b1, b2= self.tileB().segment( self._segmentB )
        xb1, yb1= b1
        xb2, yb2= b2
        return [
            ((xa1+xb2)/2, (ya1+yb2)/2),
            ((xb1+xa2)/2, (yb1+ya2)/2)
        ]
    
    # Construction: