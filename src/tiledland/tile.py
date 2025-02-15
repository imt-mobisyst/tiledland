import math
from .geometry import Float2, Shape
from .body import Body

class Tile(Body):

    def __init__( self, identifier= 0, position= Float2(0.0, 0.0), shape= None, matter= 0 ):
        super(Tile, self).__init__(identifier, position, shape, matter)
        self._adjacencies= []
        self._bodies= []

    # Accessor:    
    def adjacencies(self):
        return self._adjacencies

    def bodies(self) :
        return self._bodies
    
    def count(self) :
        return len( self._bodies)
    
    def body(self, i=1) :
        return self._bodies[i-1]
    
    # Construction:
    def setAdjacencies( self, aList ):
        self._adjacencies= aList
        return self
    
    # Connection:
    def connect(self, iTo):
        if iTo not in self._adjacencies :
            self._adjacencies.append(iTo)
            self._adjacencies.sort()
        return self

    def connectAll( self, aList ):
        for iTo in aList :
            self.connect( iTo )
        return self
    
    # Body managment
    def append(self, aPod, brushId=0, shapeId=0 ): 
        self._bodies.append( aPod )
        return self
    
    def clear(self):
        self._bodies = []
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

        # absobj interface: 
    def wordAttributes(self):
        return ["Tile"]
    
    def intAttributes(self):
        return super(Tile, self).intAttributes() + self.adjacencies()
        
    def children(self):
        return [ self.shape() ] + self.bodies()
    
    def initializeFrom( self, absObj, bodyConstructor= Body ):
        integers= absObj.intAttributes()
        children= absObj.children()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setPosition( Float2().fromList( absObj.floatAttributes() ) )
        self.setAdjacencies( integers[2:] )
        self.setShape( Shape().initializeFrom( children[0] ) )
        for absBod in children[1:] :
            self.append( bodyConstructor().initializeFrom( absBod ) )
        return self
    
    # to str
    def str(self, typeName="Tile"): 
        print( f"str(tile):" )
        # Myself :
        s= super(Tile, self).str(typeName)
        s+= " adjs"+ str(self._adjacencies)
        s+= f" bodies({ len(self.bodies()) })"
        print( f"> "+s )
        return s
    
    def __str__(self): 
        return self.str()
    