from shapely.geometry import Point, Polygon
import math

def pointFromAngle(aRadAngle, aDistance= 1.0 ):
    return Point( math.cos( aRadAngle ) * aDistance,
                    math.sin( aRadAngle ) * aDistance )

def pointRounded(aPoint, precision=2):
    return Point(round( aPoint.x, precision ), round( aPoint.y, precision ))

def pointAddition(aRadAngle, aDistance= 1.0 ):
    return Point( math.cos( aRadAngle ) * aDistance,
                    math.sin( aRadAngle ) * aDistance )

class Box():

    # Initialization Destruction:
    def __init__( self, listOfPoint=[Point(0.0, 0.0)] ):
        self.fromList( listOfPoint )

    # initialization:
    def fromList( self, listOfPoint= [Point(0.0, 0.0)] ):
        minX, minY= listOfPoint[0].x, listOfPoint[0].y
        maxX, maxY= listOfPoint[0].x, listOfPoint[0].y
        for p in listOfPoint :
            if p.x < minX :
                minX= p.x
            if p.y < minY :
                minY= p.y
            if p.x > maxX :
                maxX= p.x
            if p.y > maxY :
                maxY= p.y
        self._min= Point(minX, minY)
        self._max= Point(maxX, maxY)
        return self

    def fromShape( self, aShape ):
        pList= []
        for p in aShape.points() :
            pList.append( Point( p.x(), p.y() ) )
        if len(pList) == 0 :
            return self.fromList() 
        return self.fromList( pList ) 

    # Accessors
    def leftFloor(self):
        return self._min
    
    def rightCeiling(self):
        return self._max

    # Construction:
    def round(self, precition=0):
        self._min= pointRounded(self._min, precition)
        self._max= pointRounded(self._max, precition)
        return self
    
    def move(self, aPoint):
        self._min= Point(
            self._min.x+aPoint.x,
            self._min.y+aPoint.y
        )
        self._max= Point(
            self._max.x+aPoint.x,
            self._max.y+aPoint.y
        )
        return self
    
    def merge( self, another ):
        self._min= Point(
            min( self._min.x, another._min.x ),
            min( self._min.y, another._min.y )
        )
        self._max= Point( 
            max( self._max.x, another._max.x ),
            max( self._max.y, another._max.y )
        )
        return self
    
    # Transform:
    def asList(self):
        return [float(self._min.x), float(self._min.y)] + [float(self._max.x), float(self._max.y)]
    
    def asZip(self):
        return [(float(self._min.x), float(self._min.y)), (float(self._max.x), float(self._max.y))]
    
    # Comparison:
    def __eq__(self, another):
        return ( self._min == another.leftFloor()
            and self._max == another.rightCeiling()
        )

    # to str
    def str(self): 
        # Myself :
        min= (
            round(float(self._min.x), 2),
            round(float(self._min.y),2)
        )
        max= (
            round(float(self._max.x), 2),
            round(float(self._max.y),2)
        )
        s= f"⌊{min}, {max}⌉"
        return s
    
    def __str__(self): 
        return self.str()
