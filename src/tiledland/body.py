from .geometry import Float2, Shape
from .pod import Podable, Pod

class Body(Podable):

    # Initialization Destruction:
    def __init__( self, identifier= 0, position= Float2(0.0, 0.0), shape= None, matter= 0 ):
        self._id= identifier
        self._matter= matter
        self._center= Float2( position.x(), position.y() )
        self._shape= shape
        if self._shape is None :
            self._shape= Shape()

    # Accessor: 
    def id(self):
        return self._id
    
    def matter(self):
        return self._matter
    
    def shape(self):
        return self._shape
    
    def position(self):
        return self._center
    
    # Shape accessor : 
    def envelope(self):
        x, y= self._center.asTuple()
        return [ (x+p.x(), y+p.y()) for p in self._shape.points() ]
    
    def box(self):
        return self.shape().box().move(self.position())
    
    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setMatter(self, aInteger):
        self._matter= aInteger
        return self
    
    def setPosition(self, aFloat2):
        self._center= aFloat2
        return self
    
    def setShape(self, aShape):
        self._shape= aShape
        return self
    
    def setShapeRegular(self, size= 1.0):
        self._shape.initializeSquare(size)
        return self

    def setShapeRegular(self, numberOfVertex= 6, size= 1.0):
        self._shape.initializeRegular( numberOfVertex, size)
        return self

    # Pod interface:
    def asPod(self):
        return Pod().fromLists( 
            ["Body"], 
            [self.id(), self.matter()],
            self.position().asList(),
            [ self.shape().asPod() ]
        )
    
    def fromPod( self, aPod ):
        integers= aPod.integers()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setPosition( Float2().fromList( aPod.values() ) )
        self.setShape( Shape().fromPod( aPod.children()[0] ) )
        return self
    
    # str:
    def str(self, typeName= "Body"): 
        return typeName + f"-{self.id()} {self.box()}"
    
    def __str__(self):
        return self.str()