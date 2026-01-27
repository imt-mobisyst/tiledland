import math
from ..pod import Podable, Pod
from .basic import Point, Line
from .box import Box

class Convex(Podable):

    # Constructor/Destructor:
    def __init__( self, aListOfPoints= [] ):
        self.initialize( aListOfPoints )
    
    def copy(self, position= Point(0.0, 0.0) ):
        cpy= type(self)()
        cpy._points= [ position + p.copy() for p in self.points() ]
        return cpy
    
    # Initialization:
    def initialize(self, aListOfPoints):
        self._points= aListOfPoints
        self.makeConvex()
        return self
    
    def initializeSquare(self, size):
        demi= size*0.5
        self._points= [
            Point( -demi, -demi ),
            Point( -demi, +demi ),
            Point( +demi, +demi ),
            Point( +demi, -demi )
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
        self.makeConvex()
        return self
    
    def forcePoints(self, points):
        self._points= points
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
        self.initialize( [ Point(x, y) for x, y in zip(listX, listY) ] )
        return self

    def asZipped(self):
        return [ (p.x(), p.y()) for p in self._points ]

    def fromZipped( self, zipedList ):
        self.initialize( [ Point(x, y) for x, y in zipedList ] )
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
    def makeConvex(self):
        removed= []

        # Safe stop :
        if self.size() == 0 :
            return removed

        # Find point with minimal x value :
        for i in range( 1, self.size() ) :
            ix= self._points[i]._x
            minx= self._points[0]._x
            if ix < minx or ( ix == minx
                             and self._points[i]._y < self._points[0]._y ) :
                p= self._points[0]
                self._points[0]= self._points[i]
                self._points[i]= p

        # Trier les points par angle
        for i in range(1, self.size()) :
            v1= self._points[i]
            for j in range( i+1, self.size() ) :
                v2= self._points[j]-self._points[0]
                if v1.crossProduct(v2) < 0.0 :
                    # Echange
                    v1= v2
                    v2= self._points[i]
                    self._points[i]= self._points[j]
                    self._points[j]= v2

        # Build convex list :
        v1= self._points[0]
        convex= [ self._points[0] ]
        for i in range( 1, self.size() ) :
            # Init:
            if len(convex) < 3 or (v1 - convex[0]).crossProduct( self._points[i]-convex[0] ) < 0.0 :
                while( len(convex) > 1) and (convex[0]-convex[1]).crossProduct( self._points[i]-convex[0] ) < 0.0 :
                    removed.append( 
                        convex.pop(0)
                    )
                convex.insert(0, self._points[i])
            else :
                removed.append( self._points[i] )
        
        self._points= [ convex[-1] ] + convex[0:-1]
        return removed

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
        minLine= Line( self._points[-1], self._points[0] )
        minDist= minLine.distancePoint(aPoint)
        p1= self._points[0]
        for p2 in self._points[1:] :
            line= Line( p1, p2 )
            dist= line.distancePoint(aPoint)
            if dist < minDist :
                minDist= dist
                minLine= line
            p1= p2
        self._trace= minLine
        return minDist

    def distanceLine(self, aLine):
        dist1= self.distancePoint( aLine.point1() )
        line1= self._trace
        minDist= self.distancePoint( aLine.point2() )
        
        if dist1 < minDist :
            minDist= dist1
            self._trace= line1
        
        minDist= min(
            minDist,
            aLine.distancePoint( self._trace.point1() ),
            aLine.distancePoint( self._trace.point2() )
        )
        
        return minDist

    def distance(self, another):
        if self.isColliding(another):
            return 0.0
        p1= self._points[-1]
        p2= self._points[0]
        l12= Line(p1, p2)
        minDist= another.distanceLine(l12)
        trace= [l12, another._trace]
        
        p1= p2
        for p2 in self._points[1:] :
            l12= Line(p1, p2)
            dist= another.distanceLine(l12)
            if dist < minDist :
                minDist= dist
                trace= [l12, another._trace]
            p1= p2
        self._trace= trace
        return minDist

    # Geometry operation
    def merge( self, another ):
        self._points+= another.points()
        return self.makeConvex()

    # to str
    def str(self, typeName="Convex"): 
        # Myself :
        s= f"{typeName} {len(self._points)}" 
        s+= str( [(round(x, 2), round(y, 2)) for x, y in self.box().asZip()] )
        return s
    
    def __str__(self): 
        return self.str()
    
    # Pod interface:
    def asPod(self):
        return Pod().fromLists( ["Convex"], [], self.asList(), [] )
    
    def fromPod( self, aPod ):
        values= aPod.values()
        self._points= [
            Point(x, y)
            for x, y in zip( values[::2], values[1::2] )
        ]
        return self
