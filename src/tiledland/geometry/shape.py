import math
from ..pod import Podable, Pod
from .point import Point, Line
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
    
    # Derivated Attributs:
    def center(self):
        box= self.box()
        return box.center()

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

    # Construction:
    def round(self, precision):
        for p in self._points :
            p.round(precision)
    
    def setOnCenter(self):
        position= self.center()
        for p in self._points :
            p.set( p._x-position._x, p._y-position._y,  )
        return position

    # Convex
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
        
    # Collision:   
    def isIncludingPoint(self, aPoint):
        # Suppose self is convex...
        if self.size() < 3 :
            return False
        p1= self._points[-1]
        for p2 in self._points :
            if (p1-p2).crossProduct( aPoint-p1 ) < 0.0 :
                return False
            p1= p2
        return True
    
    def isIncludingLine(self, aLine):
        return (
            self.isIncludingPoint( aLine.point1() ) 
            and self.isIncludingPoint( aLine.point2() )
        )

    def isCollidingLine(self, aLine):
        if self.isIncludingPoint( aLine.point1() ) or self.isIncludingPoint( aLine.point2() ) :
            return True
        p1= self._points[-1]
        for p2 in self._points :
            if aLine.isColliding( Line(p1, p2) ) :
                return True
            p1= p2
        return False
    
    def isColliding( self, another ):
        # Induce a collision at box granulatrity
        if not self.box().isColliding( another.box() ) :
            return False
        # If a point of one of them is included in the other
        for p in self._points :
            if another.isIncludingPoint(p) :
                return True
        for p in another._points :
            if self.isIncludingPoint(p) :
                return True
        # If lines collides
        p1= self._points[-1]
        for p2 in self._points :
            if another.isCollidingLine( Line(p1, p2) ) :
                return True
            p1= p2
        return False

    # Distances:
    def distancePoint(self, aPoint):
        minDist= Line( self._points[-1], self._points[0] ).distancePoint(aPoint)
        p1= self._points[0]
        for p2 in self._points[1:] :
            dist= Line( p1, p2 ).distancePoint(aPoint)
            minDist= min( minDist, dist )
            p1= p2
        self._tmpLine= Line(p1, p2)
        return minDist

    def distanceLine(self, aLine):
        dist1= self.distancePoint( aLine.point1() )
        line1= self._tmpLine
        minDist= self.distancePoint( aLine.point2() )
        
        if dist1 < minDist :
            minDist= dist1
            self._tmpLine= line1
        
        minDist= min(
            minDist,
            aLine.distancePoint( self._tmpLine.point1() ),
            aLine.distancePoint( self._tmpLine.point2() )
        )
        
        return minDist

    def distance(self, another):
        if self.isColliding(another):
            return 0.0
        p1= self._points[-1]
        p2= self._points[0]
        l12= Line(p1, p2)
        minDist= another.distanceLine(l12)
        self._tmpLine= l12
        p1= p2
        for p2 in self._points[1:] :
            l12= Line(p1, p2)
            dist= another.distanceLine(l12)
            if dist < minDist :
                minDist= dist
                self._tmpLine= l12
            p1= p2
        return minDist

    # Object operator:
    def copy(self, position= Point(0.0, 0.0) ):
        cpy= type(self)()
        cpy._points= [ position + p.copy() for p in self.points() ]
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
