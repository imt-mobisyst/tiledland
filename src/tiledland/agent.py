from .geometry import Float2, Shape
from .pod import Podable, Pod

class Agent(Podable):

    # Initialization Destruction:
    def __init__( self, identifier= 0, group=0, position= Float2(0.0, 0.0), shape= None):
        self._id= identifier
        self._group= group
        self._tile= 0
        self._center= Float2( position.x(), position.y() )
        self._shape= shape
        if self._shape is None :
            self._shape= Shape().initializeSquare(0.4)
        self._matter= 10+group

    # Accessor: 
    def group(self):
        return self._group
    
    def id(self):
        return self._id
    
    def tile(self):
        return self._tile
    
    def matter(self):
        return self._matter
    
    def shape(self):
        return self._shape
    
    def position(self):
        return self._center
    
    # Shape accessor : 
    def envelope(self):
        cx, cy= self._center.asTuple()
        return Shape().fromZipped([ (cx+x, cy+y) for x, y in self._shape.asZipped() ])
    
    def box(self):
        return self.shape().box().move(self.position())
    
    def radius(self):
        r= 0.0
        zero= Float2()
        for p in self._shape._points :
            d= zero.distance( p )
            r= max( d, r )
        return r

    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setGroup(self, aInteger):
        self._group= aInteger
        return self
    
    def setTile(self, aInteger):
        self._tile= aInteger
        return self
    
    def setPosition(self, aFloat2):
        self._center= aFloat2
        return self
    
    def setMatter(self, aInteger):
        self._matter= aInteger
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
            ["Agent"], 
            [self.id(), self.group(), self.matter(), self.tile()],
            self.position().asList(),
            [ self.shape().asPod() ]
        )
    
    def fromPod( self, aPod ):
        integers= aPod.integers()
        self.setId( integers[0] )
        self.setGroup( integers[1] )
        self.setMatter( integers[2] )
        self.setTile( integers[3] )
        self.setPosition( Float2().fromList( aPod.values() ) )
        self.setShape( Shape().fromPod( aPod.children()[0] ) )
        return self
    
    # str:
    def str(self, typeName= "Agent"): 
        if self.group() :
            return typeName + f"-{self.group()}.{self.id()} {self.box()}"
        return typeName + f"-{self.id()} {self.box()}"
        
    def __str__(self):
        return self.str()