from .geometry import Float2, Shape
from .absobj import AbsObj

class Body(AbsObj):

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
        x, y= self._center.tuple()
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
    
    # absobj interface: 
    def wordAttributes(self):
        return ["Body"]
    
    def intAttributes(self):
        return [self.id(), self.matter()]
    
    def floatAttributes(self):
        return self.position().list()
    
    def children(self):
        return [self.shape()]
    
    def initializeFrom( self, aPod ):
        integers= aPod.intAttributes()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setPosition( Float2().fromList( aPod.floatAttributes() ) )
        self.setShape( Shape().initializeFrom( aPod.children()[0] ) )
        return self
    
    # str:
    def str(self, typeName= "Body"): 
        return typeName + f"-{self.id()} {self.box()}"
    
    def __str__(self):
        return self.str()