import math

class Point():
    # Initialization Destruction:
    def __init__( self, x= 0.0, y=0.0 ):
        self._x= float(x)
        self._y= float(y)

    def fromPoints(self, p1, p2):
        self._x= p2._x - p1._x
        self._y= p2._y - p1._y
        return self
    
    # Accessors
    def x(self):
        return self._x
    
    def y(self):
        return self._y
    
    # Transform :
    def asTuple(self): 
        return (self._x, self._y)
    
    def asList(self): 
        return [self._x, self._y]
    
    # Construction
    def setx(self, value):
        self._x= value
        return self
    
    def sety(self, value):
        self._y= value
        return self

    def set( self, x, y ):
        return self.setx(x).sety(y)
    
    def round( self, precision=0 ):
        self._x= round( self._x, precision )
        self._y= round( self._y, precision )
        return self
    
    def fromList( self, aList ):
        return self.setx( aList[0] ).sety( aList[1] )
    
    def fromTrigo( self, aRadAngle, aDistance= 1.0 ):
        self._x= math.cos( aRadAngle ) * aDistance
        self._y= math.sin( aRadAngle ) * aDistance
        return self

    # Object operator:
    def copy(self):
        cpy= type(self)()
        cpy._x= self.x()
        cpy._y= self.y()
        return cpy
    
    # Operator: 
    def add(self, another):
        self._x+=another._x
        self._y+=another._y
        return self

    def __add__(self, another):
        return Point( self._x+another._x,  self._y+another._y )

    def __sub__(self, another):
        return Point( self._x-another._x,  self._y-another._y )

    #Comparison:
    def __eq__(self, another):
        return ( self.x() == another.x()
            and self.y() == another.y()
        )

    def distanceSquare(self, another):
        delta= another - self
        dx, dy = delta.asTuple()
        return dx*dx + dy*dy
     
    def distance(self, another):
        delta= another - self
        dx, dy = delta.asTuple()
        return math.sqrt( dx*dx + dy*dy )
    
    # Trigo
    def norm2(self):
        return self._x*self._x + self._y*self._y
    
    def length(self):
        return math.sqrt( self.norm2() )

    def crossProduct(self, another):
        return (self._x * another._y - self._y * another._x)
    
    def dotProduct(self, another):
        return (self._x * another._x + self._y * another._y)
    
    def angleAbs(self, another):
        dot = self.dotProduct(another)
        n1 = self.length()
        n2 = another.length()
        cos_theta = dot / (n1 * n2)
        cos_theta = max( min(cos_theta, 1.0), -1.0)
        return  math.acos(cos_theta)
    
    def angle(self, another):
        dot = self.dotProduct(another)
        cross = self.crossProduct(another)
        angle = math.atan2(cross, dot)  # retourne [-pi, pi]
        return angle

        dot = self.dotProduct(another)
        n1 = self.length()
        n2 = another.length()
        cos_theta = dot / (n1 * n2)
        cos_theta = max( min(cos_theta, 1.0), -1.0)
        return  math.acos(cos_theta)
    
    def angleClockwise(self, another):
        a= self.angle(another)
        if a == 0.0 :
            return a
        if a < 0.0 :
            return -a
        return 2*math.pi-a
    
    # Collision
    def isColliding(self, point, distance=0.001):
        between= point - self
        return ( between.norm2() < (distance * distance) )

    def isCollidingLine(self, a, b, distance=0.001):
        vab= b-a
        v1= a-self
        v2= b - self
        return ( v1.length() + v2.length() ) < vab.length() + distance

    # list of points:
    def isClockwise(self, another):
        return self.crossProduct(another) < 0.0
    
    def isCounterClockwise(self, another):
        return self.crossProduct(another) > 0.0
    
    def sortRadial( self, points ):
        size= len(points)
        
        # Find point minimal distance to the left-bottom corner :
        corner= Point(
            min( [ p.x() for p in points ] ),
            min( [ p.y() for p in points ] )
        )
        minDist2= corner.distanceSquare( points[0] )
        for i in range(1, size) :
            dist2= corner.distanceSquare( points[i] )
            if dist2 < minDist2 :
                p= points[0]
                points[0]= points[i]
                points[i]= p
                minDist2= dist2

        # compute angles :
        ref= points[0]-self
        angles= [ ref.angleClockwise( p-self ) for p in points ]
        
        # Sort points by angles
        notok= True
        while notok :
            notok= False
            for i in range(size-2, 0, -1) :
                if angles[i] > angles[i+1] :
                    a= angles[i+1]
                    p= points[i+1]
                    angles[i+1]= angles[i]
                    points[i+1]= points[i]
                    angles[i]= a
                    points[i]= p
                    notok= True
        return points

    # to str
    def str(self): 
        # Myself :
        s= f"({round(self.x(), 2)}, {round(self.y(), 2)})"
        return s
    
    def __str__(self): 
        return self.str()

class Line :
    # Initialization Destruction:
    def __init__( self, a= Point(), b= Point()):
        self._p1= a
        self._p2= b

    # Accessors
    def point1(self):
        return self._p1

    def point2(self):
        return self._p2
    
    def vector(self):
        return self._p2 - self._p1
    
    def lenght(self):
        return self.vector().length()
    
    # Trigo
    def determinant(self):
        return (self.point1()._x * self.point2()._y
                - self.point1()._y * self.point2()._x)
    
    def denominator(self):
        dx = self._p2._x - self._p1._x
        dy = self._p2._y - self._p1._y
        return dx*dx + dy*dy

    def projectionPoint(self, point):
        dx = self._p2._x - self._p1._x
        dy = self._p2._y - self._p1._y
        denom= dx*dx + dy*dy

        if denom == 0:
            return self._p1.copy()

        t = ((point._x - self._p1._x) * dx + (point._y - self._p1._y) * dy)
        t/= denom
        t = max(0.0, min(1.0, t))

        return Point(self._p1._x + t*dx, self._p1._y + t*dy)
    
    def distancePoint(self, p):
        line= Line( p, self.projectionPoint(p) )
        return line.lenght()

    # Collision
    def isColliding( self, another, collide= Point(), distance=0.001 ):
        x_diff = Point( self.point1()._x - self.point2()._x, another.point1()._x - another.point2()._x)
        y_diff = Point( self.point1()._y - self.point2()._y, another.point1()._y - another.point2()._y)

        divisor = Line(x_diff, y_diff).determinant()
        if divisor == 0:
            return False

        d = Point( self.determinant(), another.determinant() )
        collide._x = Line(d, x_diff).determinant() / divisor
        collide._y = Line(d, y_diff).determinant() / divisor
        
        return (
            collide.isCollidingLine( self.point1(), self.point2(), distance )
            and collide.isCollidingLine( another.point1(), another.point2(), distance )
        )
    
    # to str
    def str(self): 
        # Myself :
        s= f"{self.point1()}->{self.point2()}"
        return s
    
    def __str__(self): 
        return self.str()