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
    
    def segments(self):
        a1, a2= self.tileA().segment( self._segmentA )
        b1, b2= self.tileB().segment( self._segmentB )
        return [
            (a1, a2 ),
            (a2, b1),
            (b1, b2),
            (b2, a1)
        ]
    
    # Construction: