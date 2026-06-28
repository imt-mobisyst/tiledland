import math, hacka
from .geometry import Point, Convex
from .artist import palette

class Entity() :
    defaultShape= Convex().initArrowTip(1.0)

    # Initialization Destruction:
    def __init__( self, identifier= 0, group=0, shape= None):
        self._id= identifier
        self._group= group
        self._refShape= shape
        if self._refShape is None :
            self._refShape= Entity.defaultShape
        self._pos= Point(0.0, 0.0)
        self._body= self._refShape.copy( self._pos )
        self._theta= 0.0
        self._brush= palette.foreground[group]
    
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
        return self._refShape

    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setGroup(self, aInteger):
        self._group= aInteger
        return self
    
    def setShape(self, aConvex):
        self._refShape= aConvex
        self._body= self._refShape.copy()
        self.setPose( self._pos, self._theta )
        return self
        
    # Transformation: 
    def setPose(self, position, angle):
        self._body.initAs( self._refShape )
        self._body.rotate( angle )
        self._theta= angle
        self._body.translate( position )
        self._pos= position
        return self

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
    def draw(self, artist):
        pass
    
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
