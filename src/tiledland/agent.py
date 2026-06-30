import hacka
from .geometry import Point, Convex
from .entity import Entity

class Agent(Entity):
    def __init__( self, identifier= 0, group=0, shape= None):
        super().__init__(identifier, group, shape)
        self._tile= 0

    # Accessor:
    def tile(self):
        return self._tile

    # Construction:    
    def setTile(self, aInteger):
        self._tile= aInteger
        return self
    
    # Hacka.DataTree interface:
    def asDataTree(self):
        x, y= self.position().asTuple()
        return hacka.DataTree(
            "Agent", 
            [self.id(), self.group(), self.tile()],
            [x, y, self.orientation()],
            [ self.referenceShape().asDataTree() ]
        )
    
    def fromDataTree( self, aDataTree ):
        digits= aDataTree.digits()
        values= aDataTree.values()
        self.setId( digits[0] )
        self.setGroup( digits[1] )
        self.setTile( digits[2] )
        self._refShape.fromDataTree( aDataTree.children()[0] )
        self.setPose( Point(values[0], values[1]), values[2] )
        return self
    
    # Agent Model:
    def process(self, perception):
        return None
    
    # str:    
    def __str__(self):
        return self.str("Agent")