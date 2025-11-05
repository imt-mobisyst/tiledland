import math
from .geometry import Point, Polygon, Box
from .pod import Podable, Pod

class Shaped(Podable):

    # Initialization Destruction:
    def __init__( self, points= None, matter= 0 ):
        if points == None :
            self._numberOfVertex= 0
            self._shape= None
        else :
            self.initializePoints(points)
        self._matter= matter
    
    # Initialization:
    def initializePoints(self, points):
        self._numberOfVertex= len(points)
        assert( self._numberOfVertex > 2 )
        self._shape= Polygon( [(p.x, p.y) for p in points ] )
        return self

    def initializeListXY(self, xList, yList):
        assert( xList[0] == xList[-1] )
        assert( yList[0] == yList[-1] )
        return self.initializePoints(
            [ Point(x, y) for x, y in zip(xList[:-1], yList[:-1]) ]
        )

    def initializeSquare(self, size):
        demi= size*0.5
        self._shape= Polygon([
                ( -demi, +demi ), ( +demi, +demi ),
                ( +demi, -demi ), ( -demi, -demi )
            ])
        self._numberOfVertex= 4
        return self

    def initializeRegular(self, size, numberOfVertex):
        radius= size*0.5
        points= []
        delta= math.pi/(numberOfVertex/2)
        angle= math.pi  - delta/2
        delta= math.pi/(numberOfVertex/2)
        for i in range(numberOfVertex) :
            points.append(
                ( math.cos(angle)*radius, math.sin(angle)*radius)
            )
            angle+= -delta
        self._shape= Polygon( points )
        self._numberOfVertex= numberOfVertex
        return self

    # Accessor: 
    def centroid(self):
        return self._shape.centroid 
    
    def shape(self):
        return self._shape
    
    def listXY(self):
        if self._shape == None :
            return [[], []]
        return self._shape.exterior.xy
        
    def numberOfVertex(self):
        return self._numberOfVertex

    def matter(self):
        return self._matter

    # Morphing
    def asPoints(self):
        xys= self.listXY()
        return [Point(x, y) for x, y in zip(xys[0][:-1], xys[1][:-1])]

    def asZip(self):
        xys= self.listXY()
        return [(x, y) for x, y in zip(xys[0][:-1], xys[1][:-1])]

    def asRoundedZip(self, epsi=2):
        xys= self.listXY()
        return [(round(float(x), epsi), round(float(y), epsi)) for x, y in zip(xys[0][:-1], xys[1][:-1])]

    def asBox(self):
        return Box( self.asPoints() )
    
    # Transformation
    def move( self, coord ):
        self._shape= Polygon( [(p.x+coord.x, p.y+coord.y) for p in self.asPoints() ] )
        return self

    # String
    def str(self, name="Shape"): 
        # Myself :
        s= f"{name} {self.numberOfVertex()}" 
        s+= str( [(round(x, 2), round(y, 2)) for x, y in self.asBox().asZip()] )
        return s
    
    def __str__(self): 
        return self.str()

    # Pod Interface:
    def asPod(self):
        xy= self.listXY()
        l= [ float(v) for v in xy[0][:-1]+xy[1][:-1] ]
        return Pod().fromLists( ["Shape"], [], l, [] )
    
    def fromPod( self, aPod ):
        values= aPod.values()
        num= len(values)//2
        points= [
            Point(x, y)
            for x, y in zip( values[:num], values[num:] )
        ]
        self.initializePoints(points)
        return self
