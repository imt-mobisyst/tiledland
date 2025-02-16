import math
from .pod import Pod
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

    # Pod interface:
    def asPod(self):
        return Pod().fromLists(  
            ["Tile"], 
            [self.id(), self.matter()] + self.adjacencies(),
            self.position().asList(),
            [self.shape().asPod()] + [ bod.asPod() for bod in self.bodies() ]
        )
    
    def fromPod( self, aPod, bodyConstructor=Body ):
        integers= aPod.integers()
        children= aPod.children()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setAdjacencies( integers[2:] )
        self.setPosition( Float2().fromList( aPod.values() ) )
        self.setShape( Shape().fromPod( aPod.children()[0] ) )
        self.clear()
        for podBod in children[1:] :
            self.append( bodyConstructor().fromPod( podBod ) )
        return self
    
    # to str
    def str(self, typeName="Tile"): 
        # Myself :
        s= super(Tile, self).str(typeName)
        s+= " adjs"+ str(self._adjacencies)
        s+= f" bodies({ len(self.bodies()) })"
        return s
    
    def __str__(self): 
        return self.str()
    