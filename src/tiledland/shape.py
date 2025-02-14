import math
from hacka.py import pod

class Float2():
    # Initialization Destruction:
    def __init__( self, x= 0.0, y=0.0 ):
        self._x= x
        self._y= y

    # Accessors
    def x(self):
        return self._x
    
    def y(self):
        return self._y
    
    def tuple(self): 
        return self._x, self._y
    
    # Construction
    def setx(self, value):
        self._x= value
        return self
    
    def sety(self, value):
        self._y= value
        return self

    def set( self, x, y ):
        return self.setx(x).sety(y)
    
    def round(self, precision):
        self._x= round( self._x, precision )
        self._y= round( self._y, precision )

    # Operator: 
    def __add__(self, another):
        return Float2( self._x+another._x,  self._y+another._y )

    def __sub__(self, another):
        return Float2( self._x-another._x,  self._y-another._y )

    #Comparison:

    def distance(self, another):
        delta= another - self
        dx, dy = delta.tuple()
        return math.sqrt( dx*dx + dy*dy )
    
class Shape(pod.PodInterface):

    # Initialization Destruction:
    def __init__( self, matter= 0, size= 1.0 ):
        self._matter= matter
        self.setShapeSquare( size )

    # Accessor:
    def points(self):
        return self._points

    def matter(self):
        return self._matter

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
    def setMatter(self, m):
        self._matter= m
        return self
    
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
        s= f"{name}-{self.matter()}/{len(self._points)} " 
        s+= str( [(round(corner.x(), 2), round(corner.y(), 2)) for corner in self.box()] )
        return s
    
    def __str__(self): 
        return self.str()
    
    # Pod interface:
    def asPod(self, family="Shape"):
        tilePod= pod.Pod(
            family,
            "",
            [self.matter()],
            self.pointsAsList()
        )
        return tilePod
    
    def fromPod(self, aPod):
        # Convert flags:
        self._matter= aPod.flag(1)
        # Convert Values:
        vals= aPod.values()
        xs= [ vals[i] for i in range( 0, len(vals), 2 ) ]
        ys= [ vals[i] for i in range( 1, len(vals), 2 ) ]
        self._points= [ Float2(x, y) for x, y in zip(xs, ys) ]
        return self
