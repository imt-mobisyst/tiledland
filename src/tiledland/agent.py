from .geometry import Point, Polygon, Box
from .shaped import Shaped
from .pod import Podable, Pod

class Agent(Podable):

    # Initialization Destruction:
    def __init__( self, identifier= 0, group=0, position= Point(0.0, 0.0), shape= None):
        self._id= identifier
        self._group= group
        self._tile= 0
        self._center= Point( position.x, position.y )
        self._shape= shape
        if self._shape is None :
            self._shape= Shaped().initializeSquare(0.4)
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
        cx, cy= self._center.x, self._center.y
        return [ (cx+x, cy+y) for x, y in self._shape.asZipped() ]
    
    def box(self):
        return Box().fromShape( self.shape() ).move(self.position())
    
    def radius(self):
        r= 0.0
        zero= Point(0.0, 0.0)
        for p in self._shape._points :
            p= Point( p.x(), p.y() )
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

    def setPosition(self, aPoint):
        assert( type(aPoint) == Point )
        self._center= Point( aPoint.x,  aPoint.y )
        return self

    def setPositionOn(self, x, y):
        return self.setPosition( Point(x, y) )
    
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
            [self.position().x, self.position().y],
            [ self.shape().asPod() ]
        )
    
    def fromPod( self, aPod ):
        integers= aPod.integers()
        self.setId( integers[0] )
        self.setGroup( integers[1] )
        self.setMatter( integers[2] )
        self.setTile( integers[3] )
        self.setPosition( Point( aPod.values()[0], aPod.values()[1] ) )
        self.setShape( Shaped().fromPod( aPod.children()[0] ) )
        return self
    
    # str:
    def str(self, typeName= "Agent"): 
        if self.group() :
            return typeName + f"-{self.group()}.{self.id()} {self.box()}"
        return typeName + f"-{self.id()} {self.box()}"
        
    def __str__(self):
        return self.str()