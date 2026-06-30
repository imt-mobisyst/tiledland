import math, hacka
from .geometry import Point, Convex
from .artist import palette

class Entity() :
    defaultShape= Convex().initArrowTip(1.0)

    # Initialization Destruction:
    def __init__( self, identifier= 0, group=0, shape= None):
        self._id= identifier
        self._refShape= shape
        if self._refShape is None :
            self._refShape= Entity.defaultShape
        self._pos= Point(0.0, 0.0)
        self._body= self._refShape.copy()
        self._theta= 0.0
        self.setGroupAndBrush(group)
    
    # Accessor: 
    def id(self):
        return self._id

    def group(self):
        return self._group
    
    def referenceShape(self):
        return self._refShape
    
    def orientation(self):
        return self._theta

    def position(self):
        return self._pos
    
    def body(self):
        return self._body

    def brush(self):
        return self._brush

    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setGroup(self, aInteger):
        self._group= aInteger
        return self
    
    def setShape(self, aConvex):
        self._refShape= aConvex
        self.updateBody()
        return self
    
    def setBody(self, aConvex):
        self._body= aConvex
        x, y= self._body.center().asTuple()
        self._position= Point(x, y)
        self._refShape= self._body.copy()
        self._refShape.translate( Point( -x, -y ) )
        self._orientation= 0.0
    
    def setShapeSquare(self, size):
        self._refShape.initSquare(size)
        self.updateBody()
        return self

    def setShapeRegular(self, size, numberOfVertex= 6):
        self._refShape.initRegular(size, numberOfVertex)
        self.updateBody()
        return self
   
    def setShapeArrowTip(self, size, theta= 0.0):
        self._refShape.initArrowTip(self, size, theta)
        self.updateBody()
        return self
    
    def updateBody(self):
        self._body= self._refShape.copy()
        self.setPose( self._pos, self._theta )
        return self

    # Convex accessor : 
    def box(self):
        return self.body().box()
    
    def radius(self):
        r= 0.0
        zero= Point()
        for p in self.referenceShape().points() :
            d= zero.distance( p )
            r= max( d, r )
        return r

    # Transformation: 
    def setPose(self, position, angle):
        self._body.initAs( self._refShape )
        self._body.rotate( angle )
        self._theta= angle
        self._body.translate( position )
        self._pos= position
        return self

    def setPosition(self, x, y):
        return self.setPose( Point(x, y), self._theta )

    def setOrientation(self, angle):
        return self.setPose( self._pos, angle )

    def translate(self, vector2):
        for p in self._body.points() :
            p.translate(vector2)
        self._pos+= vector2
        return self

    def rotate(self, angle):
        self._theta+= angle
        v2pi= 2*math.pi
        while self._theta > v2pi :
            self._theta-= v2pi
        while self._theta < -v2pi :
            self._theta+= v2pi
        self.setPose( self._pos, self._theta )
        return self

    # Artist :
    def setGroupAndBrush(self, aGroupId):
        iBrush= aGroupId%len(palette.foreground)
        self._brush= palette.foreground[iBrush]
        self._group= aGroupId
        return self
    
    # Artist drawing:
    def renderOn( self, artist ):
        artist.fillConvex( self.body(), self.brush() )
        minx, miny= self.box().leftFloor().asTuple()
        x, y= self.position().asTuple()
        artist.write( x, y, str(self.id()), self.brush() )
        return self
    
    # Hacka.DataTree interface:
    def asDataTree(self):
        return hacka.DataTree( 
            "Entity", 
            [self.id(), self.group()],
            self.position().asList(),
            [ self.shape().asDataTree() ]
        )

    def fromDataTree( self, aDataTree ):
        digits= aDataTree.digits()
        self.setId( digits[0] )
        self.setGroup( digits[1] )
        self.setMatter( digits[2] )
        self.setTile( digits[3] )
        self.setPosition( Point().fromList( aDataTree.values() ) )
        self.setShape( Convex().fromDataTree( aDataTree.children()[0] ) )
        return self
    
    def dataTreeCopy(self):
        cpy= type(self)()
        cpy.fromDataTree( self.asDataTree() )
        return cpy

    # str:
    def str(self, typeName): 
        if self.group() :
            return typeName + f"-{self.group()}.{self.id()} {self.box()}"
        return typeName + f"-{self.id()} {self.box()}"
    
    def __str__(self):
        return self.str("Entity")