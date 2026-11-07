import math
from .geometry import radian, Point, Box, Convex
from . import artist

#_defaultOutline= Convex().initRegular(1.0, 3)
_defaultOutline= Convex().initSquare(1.0)

class AbsShaped :
    
    # Shape Accessor: 
    def position(self):
        assert( "Should be implemented, and return a geometry::Point" == False )

    def orientation(self):
        assert( "Should be implemented, and return a radian angle" == False )

    def box(self):
        assert( "Should be implemented, and return a geometry::Box" == False )

    def radius(self):
        assert( "Should be implemented, and return a geometry::Point" == False )

    def convexhull(self):
        assert( "Should be implemented, and return a geometry::Point" == False )

    # test : 
    def isValidShaped(self):
        try:
            xy= self.position()
            theta= self.orientation()
            box= self.box()
            r= self.radius()
            conv= self.convexhull()
        except:
            return False
        return True

class Rectangle(AbsShaped) :
    # Constructor
    def __init__(self, width=1.0, height= 1.0):
        self._halfWidth= width*0.5
        self._halfHeight= height*0.5
        self._position= Point()
    
    # Shape Accessor: 
    def position(self):
        return self._position

    def orientation(self):
        return 0.0

    def box(self):
        x, y= self._position.asTuple()
        return Box([
            Point( x-self._halfWidth, y-self._halfHeight ),
            Point( x+self._halfWidth, y+self._halfHeight )
        ])

    def radius(self):
        return math.sqrt( self._halfWidth*self._halfWidth + self._halfHeight*self._halfHeight )
    
    def convexhull(self):
        x, y= self._position.asTuple()
        x1= x-self._halfWidth
        y1= y-self._halfHeight
        x2= x+self._halfWidth
        y2= y+self._halfHeight
        return Convex([
            Point( x1, y1 ),
            Point( x1, y2 ),
            Point( x2, y2 ),
            Point( x2, y1 )
        ])

    # Construction:
    def setPosition(self, p):
        self._position= p
        return self
    