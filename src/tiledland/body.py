from .geometry import Float2, Shape


class Body():

    # Initialization Destruction:
    def __init__( self, identifier= 0, position= Float2(0.0, 0.0), shape= Shape(), matter= 0 ):
        self._id= identifier
        self._matter= matter
        self._center= Float2( position.x(), position.y() )
        self._shape= shape

    # Accessor: 
    def id(self):
        return self._id
    
    def matter(self):
        return self._matter
    
    def shape(self):
        return self._shape
    
    def position(self):
        return self._center
    
    def envelope(self):
        x, y= self._center.tuple()
        return [ (x+p.x(), y+p.y()) for p in self._shape.points() ]
    
    # Construction:
    def setId(self, aInteger):
        self._id= aInteger
        return self
    
    def setMatter(self, aInteger):
        self._matter= aInteger
    
    def setPosition(self, aFloat2):
        self._position= aFloat2
        return self
    
    def setShape(self, aShape):
        self._shape= aShape
        return self
    
    # Pod interface: 
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
    
    # str:
    def str(self): 
        return str(self.id()) + " on "+ str(self.position())
    
    def __str__(self):
        return self.str()