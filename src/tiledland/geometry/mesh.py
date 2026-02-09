import math

class Mesh():
    # Constructions :
    def __init__(self, pointsList= []):
        self._points= [ p for p in pointsList ]
    
    def copy(self): 
        cpy= Mesh()
        cpy._points= [ p.copy() for p in self._points ]
        return cpy
    
    # Accessors :
    def size(self):
        return len(self._points)

    def points(self):
        return self._points
    
    def point(self, i):
        return self._points[i-1]
    
    # Construction :
    def append(self, p):
        self._points.append(p)

    # Morphing :
    def asTuples(self):
        return [ p.asTuple() for p in self._points ]
    
    # Opperations :
    def round(self, floatDeep):
        for p in self._points :
            p.round(2)
        return self
    
    def searchClosestTo( self, position ):
        if self.size() == 0 :
            return 0
        d2min= position.distanceSquare( self.point(1) )
        imin= 1
        for i in range( 2, self.size()+1 ):
            d2= position.distanceSquare( self.point(i) )
            if d2 < d2min :
                imin= i
                d2min= d2
        return imin
