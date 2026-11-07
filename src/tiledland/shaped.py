import math
from .geometry import radian, Point, Box, Convex
from . import artist

#_defaultOutline= Convex().initRegular(1.0, 3)
_defaultOutline= Convex().initSquare(1.0)

class AbsShaped :
    # Constructor
    def __init__(self, owner=0, category=0, identifier=0, name="Shaped"):
        self._owner= owner
        self._category= category
        self._identifier= identifier
        self._name= name
    
    # Shape Accessor:
    def position(self):
        assert( "Should be implemented, and return a geometry::Point" == False )

    def orientation(self):
        assert( "Should be implemented, and return a radian angle" == False )

    def radius(self):
        assert( "Should be implemented, and return a positive value" == False )

    def shape(self):
        assert( "Should be implemented, and return a geometry::Convex" == False )

    # Who is Accessor:
    def owner(self):
        return self._owner

    def category(self):
        return self._category

    def identifier(self):
        return self._identifier

    def name(self):
        return self._name

    # Derivated Accessor : 
    def box(self):
        return self.shape().box()

    # Construction:
    def setOwner(self, owner):
        self._owner= owner
        return self

    def setCategory(self, aCategory):
        self._category= aCategory
        return self

    def setIdentifier(self, identifier):
        self._identifier= identifier
        return self

    def setName(self, aName):
        self._name= aName
        return self
    
    # test : 
    def isValidShaped(self):
        try:
            xy= self.position()
            theta= self.orientation()
            box= self.box()
            r= self.radius()
            conv= self.shape()
        except:
            return False
        return True

    # str:
    def str(self): 
        return self.strIdentity() + f" {self.box()}"
    
    def strIdentity(self):
        return f"{self._name} {self.owner()}-{self.identifier()}"

    def __str__(self):
        return self.str()

class Rectangle(AbsShaped) :
    # Constructor
    def __init__(self, width=1.0, height= 1.0,
            owner=0, category=0, identifier=0, name="Rectangle"):
        super().__init__(owner, category, identifier, name)
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
    
    def shape(self):
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
    