import math
from .float2 import Float2

class Box():

    # Initialization Destruction:
    def __init__( self, listOfPoint=[Float2()] ):
        self.fromList( listOfPoint )

    # initialization:
    def fromList( self, listOfPoint= [Float2()] ):
        self._min= Float2( listOfPoint[0].x(), listOfPoint[0].y() )
        self._max= Float2( listOfPoint[0].x(), listOfPoint[0].y() )
        for p in listOfPoint :
            if p.x() < self._min.x() :
                self._min.setx( p.x() )
            if p.y() < self._min.y() :
                self._min.sety( p.y() )
            if p.x() > self._max.x() :
                self._max.setx( p.x() )
            if p.y() > self._max.y() :
                self._max.sety( p.y() )
        return self
        

    # Accessors
    def leftFloor(self):
        return self._min
    
    def rightCeiling(self):
        return self._max

    # Construction:
    def round(self, precition=0):
        self._min.round(precition)
        self._max.round(precition)
        return self
    
    def move(self, aFloat2):
        self._min+= aFloat2
        self._max+= aFloat2
        return self
    
    def merge( self, another ):
        self._min._x= min( self._min._x, another._min._x )
        self._min._y= min( self._min._y, another._min._y )
        self._max._x= max( self._max._x, another._max._x )
        self._max._y= max( self._max._y, another._max._y )
        return self
    
    # Transform:
    def asList(self):
        return self._min.asList() + self._max.asList()
    
    def asZip(self):
        return [self._min.asTuple(), self._max.asTuple()]
    
    # Comparison:
    def __eq__(self, another):
        return ( self._min == another.leftFloor()
            and self._max == another.rightCeiling()
        )


    # to str
    def str(self): 
        # Myself :
        s= f"⌊{self._min}, {self._max}⌉"
        return s
    
    def __str__(self): 
        return self.str()