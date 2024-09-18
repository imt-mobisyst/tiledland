import math

class Coord2 :
    def __init__(self, x=0.0, y=0.0) -> None:
        self._x= float(x)
        self._y= float(y)

    # Construction:
    def set(self, x, y):
        self._x= x
        self._y= y

    def setAs(self, aCoord):
        self._x= aCoord._x
        self._y= aCoord._x

    def setFromTuple( self, t ):
        self._x, self._y= t
        return self

    # Deep Copy:
    def copy(self):
        return Coord2( self._x, self._y )
    
    # Accessors:
    def dimention(self):
        return 2
    
    def x(self):
        return self._x

    def y(self):
        return self._y

    def tuple(self):
        return (self._x, self._y)

    # Comparison:
    def __eq__( self, another ):
        return (self._x == another._x) and (self._y == another._y)

    def __neq__( self, another ):
        return (self._x != another._x) or (self._y != another._y)

    # Operators:
    def __add__( self, another ):
        return Coord2(
            self._x + another._x,
            self._y + another._y
        )
    
    def __sub__( self, another ):
        return Coord2(
            self._x - another._x,
            self._y - another._y
        )
    
    # Property:
    def distance(self):
        return math.sqrt( self.distanceSquare() )
    
    def distanceSquare(self):
        return self._x*self._x + self._y*self._y

    def normal(self):
        factor= 1.0/self.distance()
        return Coord2(
            self._x*factor,
            self._y*factor
        )
    
    def orthonormal(self):
        factor= 1.0/self.distance()
        return Coord2(
            -self._y*factor,
            self._x*factor
        )
    
    # Generator:

    # Transformation:
    def round( self, precision=1 ):
        return Coord2( round( self._x, precision ), round( self._y, precision ) )
    
    def scale( self, scalar ):
        return Coord2( self._x*scalar, self._y*scalar )
    
    # Print
    def __str__(self) -> str:
        return f"({self._x}, {self._y})"

class Segment :

    def __init__(self, coordinateA= Coord2(), coordinateB= Coord2()) -> None:
        self._a= coordinateA
        self._b= coordinateB

    # Construction:
    def set(self, coordinateA, coordinateB):
        self._a= coordinateA
        self._b= coordinateB
        return self

    def setAs(self, aSegment):
        self._a= aSegment._a
        self._b= aSegment._b
        return self

    def setFromList( self, l ):
        self._a= Coord2().setFromTuple( l[0] )
        self._b= Coord2().setFromTuple( l[1] )
        return self

    # Accessors:
    def dimention(self):
        return 2
    
    def a(self):
        return self._a

    def b(self):
        return self._b

    def extremities(self):
        return self._a, self._b
    
    def list(self):
        return [self._a.tuple(), self._b.tuple()]

    # Property:
    def middle(self):
        return (self._b - self._a).scale(0.5) + self._a
    
    def vector(self):
        return self._b - self._a

    # Comparison:
    def __eq__( self, another ):        
        return (self._a == another._a) and (self._b == another._b)

    def __neq__( self, another ):
        return (self._a != another._a) or (self._b != another._b)

    # Operators:

    # Transformation:
    def scale( self, scalar ):
        v= self.vector()
        demi= v.distance() * scalar * 0.5
        dir= v.normal().scale(demi)
        middle= self.middle()
        self._a= middle - dir
        self._b= middle + dir
        return self
    
    # Generators:
    def copy(self):
        return Segment( self._a.copy(), self._b.copy() )
    
    def inflate(self, thickness= 1.0):
        delta= self.vector().orthonormal().scale(thickness/2)
        return [
            self.a()-delta, self.a()+delta,
            self.b()+delta, self.b()-delta 
        ]

    # Print
    def __str__(self) -> str:
        return f"{self._a}>{self._b}"