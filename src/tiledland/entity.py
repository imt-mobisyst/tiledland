import math, hacka
from .geometry import Point, Convex
from .artist import palette, Brush

class AbsEntity() :
    def box(self):
        assert( False and "Should be defined" )
        # return a tiledland.Box object, encapsulating the entity.

    def asDataTree( self, aDataTree ):
        assert( False and "Should be defined" )
        # return a hacka.DataTree object descrybing the entity.

    def fromDataTree( self, aDataTree ):
        assert( False and "Should be defined" )
        # build the entity from a hacka.DataTree
        return self
    
    def dataTreeCopy(self):
        cpy= type(self)()
        cpy.fromDataTree( self.asDataTree() )
        return cpy
    
class Entity(AbsEntity) :
    defaultShape= Convex().initArrowTip(1.0)
    defaultPalette= palette.foreground

    # Initialization Destruction:
    def __init__( self,
            group= 0,
            shape= None,
            position= Point(0.0, 0.0), orientation= 0.0,
            brush= None,
            area=0, index= 0,
            name= "Entity"):
        self._refShape= shape
        if self._refShape is None :
            self._refShape= type(self).defaultShape
        self._brush= brush
        if self._brush is None :
            self.setGroupAndBrush(group)
        else :
            self._group= group
        assert( type(self._refShape) == Convex )
        assert( type(self._brush) == Brush )
        self._position= position.copy()
        self._theta= orientation
        self._area= area
        self._index= index
        self._projShape= Convex()
        self.setPose(self._position, self._theta)
        self._name= name
    
    def copy(self):
        return type(self)(
            self._group,
            self._refShape,
            self._position, self._theta,
            self._brush,
            self._area, self._index 
        )

    # Accessor: 
    def group(self):
        return self._group
    
    def area(self):
        return self._area
    
    def index(self):
        return self._index
    
    def location(self):
        return (self._area, self._index)

    def referenceShape(self):
        return self._refShape
    
    def orientation(self):
        return self._theta

    def position(self):
        return self._position
    
    def projectedShape(self):
        return self._projShape

    def brush(self):
        return self._brush

    # Construction:
    def setArea(self, aInteger):
        self._area= aInteger
        return self

    def setIndex(self, aInteger):
        self._index= aInteger
        return self
    
    def setLocation(self, area, index):
        self._area= area
        self._index= index
        return self
    
    def setGroup(self, aInteger):
        self._group= aInteger
        return self

    def setGroupAndBrush(self, aInteger):
        self._brush= type(self).defaultPalette[aInteger%len(type(self).defaultPalette)]
        self._group= aInteger
        return self
    
    def setReferenceShape(self, aConvex):
        self._refShape= aConvex
        self.updateProjection()
        return self
    
    def setProjectedShape(self, aConvex):
        self._projShape= aConvex
        x, y= self._projShape.center().asTuple()
        self._position= Point(x, y)
        self._refShape= self._projShape.copy()
        self._refShape.translate( Point( -x, -y ) )
        self._orientation= 0.0
    
    def setShapeSquare(self, size):
        self._refShape= Convex().initSquare(size)
        self.updateProjection()
        return self

    def setShapeRegular(self, size, numberOfVertex= 6):
        self._refShape= Convex().initRegular(size, numberOfVertex)
        self.updateProjection()
        return self
   
    def setShapeArrowTip(self, size, theta= 0.0):
        self._refShape= Convex().initArrowTip(self, size, theta)
        self.updateProjection()
        return self
    
    def updateProjection(self):
        self._projShape= self._refShape.copy()
        self.setPose( self._position, self._theta )
        return self

    # Convex accessor : 
    def box(self):
        return self.projectedShape().box()
    
    def radius(self):
        r= 0.0
        zero= Point()
        for p in self.referenceShape().points() :
            d= zero.distance( p )
            r= max( d, r )
        return r

    # Transformation: 
    def setPose(self, position, angle):
        self._projShape.initAs( self._refShape )
        if angle != 0.0 :
            self._projShape.rotate( angle )
        self._theta= angle
        if position.x() != 0.0 or position.y() != 0.0 :
            self._projShape.translate( position )
        self._position= position
        return self

    def setPosition(self, x, y):
        return self.setPose( Point(x, y), self._theta )

    def setOrientation(self, angle):
        return self.setPose( self._position, angle )

    def translate(self, vector2):
        for p in self._projShape.points() :
            p.translate(vector2)
        self._position+= vector2
        return self

    def rotate(self, angle):
        self._theta+= angle
        v2pi= 2*math.pi
        while self._theta > v2pi :
            self._theta-= v2pi
        while self._theta < -v2pi :
            self._theta+= v2pi
        self.setPose( self._position, self._theta )
        return self

    # Artist :
    def setBrush(self, aBrush):
        self._brush= aBrush
        return self
    
    def renderOn( self, artist ):
        artist.fillConvex( self.projectedShape(), self.brush() )
        minx, miny= self.box().leftFloor().asTuple()
        x, y= self.position().asTuple()
        artist.write( x, y, self._name, self.brush() )
        return self
    
    # Hacka.DataTree interface:
    def asDataTree(self):
        x, y= self.position().asTuple()
        return hacka.DataTree( 
            self._name, 
            [self.group(), self._area, self._index],
            [x, y, self.orientation()],
            [ self.referenceShape().asDataTree() ]
        )

    def fromDataTree( self, aDataTree ):
        self._name= aDataTree.label()
        digits= aDataTree.digits()
        values= aDataTree.values()
        self.setReferenceShape( Convex().fromDataTree( aDataTree.children()[0] ) )
        self.setGroup( digits[0] )
        self.setLocation( digits[1], digits[2] )
        self.setPose( Point(values[0], values[1]), values[2] )
        return self
    
    def dataTreeCopy(self):
        cpy= type(self)()
        cpy.fromDataTree( self.asDataTree() )
        return cpy

    # str:
    def str(self, typeName="Entity"): 
        return typeName + f"{self.group()} {self.area()}-{self.index()} {self.box()}"
    
    def __str__(self):
        return self.str()