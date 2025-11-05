import math
from . import geometry
from .pod import Pod
from .geometry import Point
from .shaped import Shaped
from .agent import Agent


clockAngles= [ 0.0, 2.0*math.pi/6.0, math.pi/6.0, 0.0,
               math.pi/-6.0, -2.0*math.pi/6.0, math.pi/-2.0,
               -2.0*math.pi/3.0, -5.0*math.pi/6.0, math.pi,
               5.0*math.pi/6.0, 2.0*math.pi/3.0, math.pi/2.0
               ]
clockPositions= [
    geometry.pointFromAngle(x) for x in clockAngles
]
clockLenght= 13


class Tile(Agent):

    def __init__( self, identifier= 0, position= Point(0.0, 0.0), shape= None, matter=0):
        shape
        if shape is None :
            shape= Shape().initializeSquare(1.0)
        self._adjacencies= []
        self._agents= []
        super(Tile, self).__init__(identifier, 0, position, shape)
        self._matter= matter
        
    # Accessor:
    def adjacencies(self):
        return self._adjacencies

    def agents(self) :
        return self._agents
    
    def count(self) :
        return len( self._agents)
    
    def agent(self, i=1) :
        return self._agents[i-1]
    
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
    
    def clockDirection( self, aPosition ):
        center= self.position()
        radius= self.radius()
        if center.distance( aPosition ) < radius :
            return 0
        clock= 1
        distance= aPosition.distance( Point(center.x+clockPositions[1].x, center.y+clockPositions[1].y) )
        for i in range( 2, clockLenght ):
            option= Point(center.x+clockPositions[i].x, center.y+clockPositions[i].y)
            d= aPosition.distance( option )
            if d < distance :
                clock= i
                distance= d
        return clock

    # Agent managment
    def append(self, aPod, brushId=0, shapeId=0 ): 
        self._agents.append( aPod )
        return self
    
    def clear(self):
        self._agents = []
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

    # Pod interface:
    def asPod(self):
        return Pod().fromLists(  
            ["Tile"], 
            [self.id(), self.matter()] + self.adjacencies(),
            [self.position().x, self.position().y],
            [self.shape().asPod()] + [ ag.asPod() for ag in self.agents() ]
        )
    
    def fromPod( self, aPod, agentFactory=Agent ):
        integers= aPod.integers()
        values= aPod.values()
        children= aPod.children()
        self.setId( integers[0] )
        self.setMatter( integers[1] )
        self.setAdjacencies( integers[2:] )
        self.setPositionOn( values[0], values[1] )
        self.setShape( Shape().fromPod( aPod.children()[0] ) )
        self.clear()
        for podBod in children[1:] :
            self.append( agentFactory().fromPod( podBod ) )
        return self
    
    # to str
    def str(self, typeName="Tile"): 
        # Myself :
        s= super(Tile, self).str(typeName)
        s+= " adjs"+ str(self._adjacencies)
        s+= f" agents({ len(self.agents()) })"
        return s
    
    def __str__(self): 
        return self.str()
    