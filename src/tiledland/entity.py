import hacka
from .geometry import Point, Convex

class Entity() :
    # Initialization Destruction:
    def __init__( self, identifier= 0, group=0, shape= None):
        self._id= identifier
        self._group= group
        self._shape= shape
        if self._shape is None :
            self._shape= Convex().initializeSquare(0.4)
        self._matter= 10+group
    
    # Accessor: 
    def group(self):
        return self._group
    
    def id(self):
        return self._id
    
    def shape(self):
        return self._shape
    
    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setGroup(self, aInteger):
        self._group= aInteger
        return self
    
    def setShape(self, aConvex):
        self._shape= aConvex
        return self
    
    def setShapeRegular(self, size= 1.0):
        self._shape.initializeSquare(size)
        return self

    def setShapeRegular(self, numberOfVertex= 6, size= 1.0):
        self._shape.initializeRegular( numberOfVertex, size)
        return self
    
    # Artist :
    def draw(self, artist):
        pass
    
    # Hacka.DataTree interface:
    def asDataTree(self):
        return hacka.DataTree().fromLists( 
            ["Entity"], 
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
