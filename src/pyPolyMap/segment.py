import math
from .point import Point2

class Segment:

    # Initialization Destruction:
    def __init__( self, aPoint= Point2(), anotherPoint= Point2(), tag= 0 ):
        self.set(aPoint, anotherPoint, tag)
    
    # Accessor :
    def pointA(self) : 
        return self._a
    
    def pointB(self) : 
        return self._b
    
    def center(self) :
        return (self._a + self._b).scale(0.5)
    
    def tag(self) : 
        return self._tag
    
    def lenght(self) : 
        return self._a.distance(self._b)
    
    def lenghtSquare(self) : 
        return self._a.distanceSquare(self._b)

    # Construction:
    def set( self, aPoint, anotherPoint, tag= 0 ):
        if aPoint <= anotherPoint :
            self._a= aPoint
            self._b= anotherPoint
        else :
            self._a= anotherPoint
            self._b= aPoint
        self._tag= tag
        return self
    
    def setTag( self, tag ):
        self._tag= tag
        return self

    # Operators: 

    # Scalaire: 
    
    # Comparison:
    def __eq__(self, another):
        return (
            ( self._a == another._a and self._b == another._b )
            or 
            ( self._a == another._b and self._b == another._a )
        )

    # Print:
    def __str__(self):
        return f"[{self._a}--{self._b}]"
