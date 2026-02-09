import math
from .basic import Point

class Box(): # AABB Box

    # Initialization Destruction:
    def __init__( self, listOfPoint=[Point()] ):
        self.fromList( listOfPoint )

    def copy(self):
        cpy= Box()
        cpy._min= self._min.copy()
        cpy._max= self._max.copy()
        return cpy
     
    # Initialization:
    def fromList( self, listOfPoint= [Point()] ):
        self._min= Point( listOfPoint[0].x(), listOfPoint[0].y() )
        self._max= Point( listOfPoint[0].x(), listOfPoint[0].y() )
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
    
    def width(self) :
        return self._max.x() - self._min.x()
    
    def height(self) :
        return self._max.y() - self._min.y()
    
    def dimention(self):
        return ( self.width(), self.height() )
    
    def center(self):
        v= self._max - self._min
        return self._min + Point( v.x()*0.5, v.y()*0.5 )
    
    def perimeter(self):
        return self.width()*2 + self.height()*2
    
    def score(self):
        w, h= self.width(), self.height()
        return (self.width() + self.height()) * 1 + abs(w-h)
    
    # Construction:
    def round(self, precition=0):
        self._min.round(precition)
        self._max.round(precition)
        return self
    
    def move(self, aPoint):
        self._min+= aPoint
        self._max+= aPoint
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

    # Collision:
    def isColliding(self, another):
        # no separation in anny axis
        return ( not( 
                (self._min._x <= another._min._x and self._max._x <= another._min._x )
                or (self._min._y <= another._min._y and self._max._y <= another._min._y )
                or (self._min._x > another._min._x and another._max._x < self._min._x )
                or (self._min._y > another._min._y and another._max._y < self._min._y )
            )
        )

    def isIncluding(self, another):
        # both coordinates are included
        return ( 
            ( self._min._x <= another._min._x and another._min._x < another._max._x )
            and ( self._min._y <= another._min._y and another._min._y < another._max._y )
            and ( self._min._x < another._max._x and another._max._x <= another._max._x )
            and ( self._min._y < another._max._y and another._max._y <= another._max._y )
        )
    
    # operator:
    def __add__(self, another):
        b= self.copy()
        b.merge(another)
        return b

    # to str
    def str(self): 
        # Myself :
        s= f"⌊{self._min}, {self._max}⌉"
        return s
    
    def __str__(self): 
        return self.str()