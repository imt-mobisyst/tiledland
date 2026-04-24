import hacka
from .geometry import Point, Convex
from .entity import Entity

class Agent(Entity):
    def __init__( self, identifier= 0, group=0, position= Point(0.0, 0.0), shape= None):
        super().__init__(identifier, group, shape)
        self._tile= 0
        self._center= Point( position.x(), position.y() )
        self._matter= 10+group

    
    def tile(self):
        return self._tile
    
    def matter(self):
        return self._matter
    
    def position(self):
        return self._center
    
    def body(self):
        return self._shape.copy(self._center)

    # Convex accessor : 
    def box(self):
        return self.body().box()
    
    def radius(self):
        r= 0.0
        zero= Point()
        for p in self._shape._points :
            d= zero.distance( p )
            r= max( d, r )
        return r

    # Construction:    
    def setTile(self, aInteger):
        self._tile= aInteger
        return self
    
    def setPosition(self, aPoint):
        self._center= aPoint
        return self
    
    def setMatter(self, aInteger):
        self._matter= aInteger
        return self
    
    def setBody(self, aConvex):
        self._center= aConvex.center()
        subCenter= Point( -self._center.x(), -self._center.y() )
        self._shape= aConvex.copy(subCenter) 
        return self

    # Hacka.DataTree interface:
    def asDataTree(self):
        return hacka.DataTree().fromLists( 
            ["Agent"], 
            [self.id(), self.group(), self.matter(), self.tile()],
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
    
    # str:
    def str(self, typeName= "Agent"): 
        if self.group() :
            return typeName + f"-{self.group()}.{self.id()} {self.box()}"
        return typeName + f"-{self.id()} {self.box()}"
        
    def __str__(self):
        return self.str()