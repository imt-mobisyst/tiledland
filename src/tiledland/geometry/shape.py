import math
from ..pod import Podable, Pod
from .point import Point
from .box import Box

class Shape(Podable):

    # Constructor/Destructor:
    def __init__( self, aListOfPoints= [] ):
        self.initialize( aListOfPoints )
    
    # Initialization:
    def initialize(self, aListOfPoints):
        self._points= aListOfPoints
        return self
    
    def initializeSquare(self, size):
        demi= size*0.5
        self._points= [
            Point( -demi, +demi ),
            Point( +demi, +demi ),
            Point( +demi, -demi ),
            Point( -demi, -demi )
        ]
        return self

    def initializeRegular(self, size, numberOfVertex= 6):
        radius= size*0.5
        self._points= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            p= Point( math.cos(angle)*radius, math.sin(angle)*radius)
            self._points.append(p)
            angle+= -delta
        return self
    
    # Accessor:
    def size(self):
        return len(self._points)
    
    def points(self):
        return self._points
    
    def box(self):
        if self.size() == 0 :
            return Box()
        return Box(self.points())
    
    # Morphing:
    def asList(self):
        l= []
        for p in self._points:
            l+= [p.x(), p.y()]
        return l
    
    def asLists(self, dx=0.0, dy=0.0):
        return [p.x()+dx for p in self._points], [p.y()+dy for p in self._points]
    
    def fromLists(self, listX, listY):
        self._points= [ Point(x, y) for x, y in zip(listX, listY) ]
        return self

    def asZipped(self):
        return [ (p.x(), p.y()) for p in self._points ]

    def fromZipped( self, zipedList ):
        self._points= [ Point(x, y) for x, y in zipedList ]
        return self
    
    def asConvex(self):
        assert self.size() > 0

        points= [p for p in self._points]
        size= len(points)

        # Find point with minimal x value :
        for i in range( 1, size ) :
            ix= points[i]._x
            minx= self._points[0]._x
            if ix < minx or ( ix == minx
                             and self._points[i]._y < self._points[0]._y ) :
                p= points[0]
                points[0]= points[i]
                points[i]= p

        # Trier les points par angle
        for i in range(1, size) :
            v1= points[i]
            for j in range( i+1, size ) :
                v2= points[j]-points[0]
                if v1.crossProduct(v2) < 0.0 :
                    # Echange
                    v1= v2
                    v2= points[i]
                    points[i]= points[j]
                    points[j]= v2
        
        # Build convex list :
        v1= points[0]
        convex= [ points[0] ]
        for i in range( 1, size ) :
            # Init:
            if len(convex) < 3 or (v1 - convex[0]).crossProduct( points[i]-convex[0] ) < 0.0 :
                while( len(convex) > 1) and (convex[0]-convex[1]).crossProduct( points[i]-convex[0] ) < 0.0 :
                    convex.pop(0)
                convex.insert(0, points[i])
        
        return Shape( [ convex[-1] ] + convex[0:-1] )
    
    # Construction:
    def round(self, precision):
        for p in self._points :
            p.round(precision)
    
    # Object operator:
    def copy(self):
        cpy= type(self)()
        cpy._points= [ p.copy() for p in self.points() ]
        return cpy

    # to str
    def str(self, typeName="Shape"): 
        # Myself :
        s= f"{typeName} {len(self._points)}" 
        s+= str( [(round(x, 2), round(y, 2)) for x, y in self.box().asZip()] )
        return s
    
    def __str__(self): 
        return self.str()
    
    # Pod interface:
    def asPod(self):
        return Pod().fromLists( ["Shape"], [], self.asList(), [] )
    
    def fromPod( self, aPod ):
        values= aPod.values()
        self._points= [
            Point(x, y)
            for x, y in zip( values[::2], values[1::2] )
        ]
        return self
