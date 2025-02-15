import math
from .float2 import Float2

class Shape():

    # Initialization Destruction:
    def __init__( self, size= 1.0 ):
        self.setShapeSquare( size )

    # Accessor:
    def points(self):
        return self._points
    
    def box(self):
        points= self.points()
        minPoint= Float2( points[0].x(), points[0].y() )
        maxPoint= Float2( points[0].x(), points[0].y() )
        for p in points :
            if p.x() < minPoint.x() :
                minPoint.setx( p.x() )
            if p.y() < minPoint.y() :
                minPoint.sety( p.y() )
            if p.x() > maxPoint.x() :
                maxPoint.setx( p.x() )
            if p.y() > maxPoint.y() :
                maxPoint.sety( p.y() )
        return [minPoint, maxPoint]

    def envelope(self):
        return [ (p.x(), p.y()) for p in self._points ]
    
    # list accessors: 
    def pointsAsList(self):
        l= []
        for p in self.points() :
            l+= [p.x(), p.y()]
        return l

    # Construction:
    def setEnveloppe( self, envelopes ):
        self._points= [ Float2(x, y) for x, y in envelopes ]
        return self
    
    def round(self, precision):
        for p in self._points :
            p.round(precision)

    # Shape Construction:
    def setShapeSquare(self, size):
        demi= size*0.5
        self._points= [
            Float2( -demi, +demi ),
            Float2( +demi, +demi ),
            Float2( +demi, -demi ),
            Float2( -demi, -demi )
        ]
        return self

    def setShapeRegular(self, size, numberOfVertex= 6):
        radius= size*0.5
        self._points= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            p= Float2( math.cos(angle)*radius, math.sin(angle)*radius)
            self._points.append(p)
            angle+= -delta
        return self
    
    # to str
    def str(self, name="Shape", ident=0): 
        # Myself :
        s= f"{name}-{len(self._points)} " 
        s+= str( [(round(corner.x(), 2), round(corner.y(), 2)) for corner in self.box()] )
        return s
    
    def __str__(self): 
        return self.str()
    
    # Pod interface:
        # Pod interface: 
    def wordAttributes(self):
        return ["Shape"]
    
    def intAttributes(self):
        return []
    
    def floatAttributes(self):
        l= []
        for p in self._points:
            l+= [p.x(), p.y()]
        return l
    
    def children(self):
        return []
    
    def initializeFrom( self, aPod ):
        values= aPod.floatAttributes()
        self._points= [
            Float2(x, y)
            for x, y in zip( values[::2], values[1::2] )
        ]
