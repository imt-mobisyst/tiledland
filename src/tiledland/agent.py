from .geometry import Float2, Shape

class Agent():

    # Initialization Destruction:
    def __init__( self, name= "A", position= Float2(0.0, 0.0), size= 0.5 ):
        self._name= name
        self._body= Shape().setShapeRegular( size, 8 )
        self._center= Float2( position.x(), position.y() )

    # Accessor: 
    def name(self):
        return self._name
    
    def body(self):
        return self._body
    
    def position(self):
        return self._center
    
    def envelope(self):
        x, y= self._center.tuple()
        return [ (x+p.x(), y+p.y()) for p in self._body.points() ]
    
    # Construction:
    def setName(self, name):
        self._name= name
        return self
    
    # Pod interface: 
    def wordAttributes(self):
        return ["Agent", self.name()]
    
    def intAttributes(self):
        return []
    
    def floatAttributes(self):
        return self.position().list()
    
    def children(self):
        return [ self.body() ]
    
    def initializeFrom( self, aPod ):
        self._name= aPod.wordAttributes()[1]
        self._center= Float2().fromList( aPod.floatAttributes() )
        self._body.initializeFrom( aPod.children()[0] )
    
    # str:
    def str(self): 
        return self.name() + " on "+ str(self.position())
    
    def __str__(self):
        return self.str()