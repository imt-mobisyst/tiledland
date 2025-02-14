import math
from .geometry.shape import Float2, Shape

class Tile(Shape):

    # Initialization Destruction:
    def __init__( self, num= 0, matter= 0, center= Float2(), size= 1.0 ):
        self._num= num
        self._center= Float2( center.x, center.y )
        super().__init__(size, matter)
        self._adjacencies= []
        self._agents= []

    # Accessor:
    def number(self):
        return self._num

    def center(self):
        return self._center
    
    def adjacencies(self):
        return self._adjacencies

    def envelope(self):
        cx, cy= self._center.x(), self._center.y()
        return [ (cx+p.x(), cy+p.y()) for p in self.points() ]

    def agents(self) :
        return self._agents
    
    def count(self) :
        return len( self._agents)
    
    def agent(self, i=1) :
        return self._pieces[i-1]

    def box(self):
        return [ p+self.center() for p in super().box() ]
    
    # Construction    
    def setNumber(self, i):
        self._num= i
        return self

    def setCenter(self, x, y):
        self._center= Float2(x, y)
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
    
    # Piece managment
    def append(self, aPod, brushId=0, shapeId=0 ): 
        self._pieces.append( aPod )
        self._piecesBrushId.append( brushId )
        self._piecesShapeId.append( shapeId )
        return self
    
    def clear(self):
        self._pieces = []
        self._piecesBrushId = []
        self._piecesShapeId = []
        return self
    
    # Comparison :
    def centerDistance(self, another):
        return self.center().distance( another.center() )

    # Pod interface:
    def initializeFrom(self, aPod):
        # Convert flags:
        flags= aPod.flags()
        self._num= flags[0]
        self._matter= flags[1]
        self._adjacencies= flags[2:]
        # Convert Values:
        vals= aPod.values()
        xs= [ vals[i] for i in range( 0, len(vals), 2 ) ]
        ys= [ vals[i] for i in range( 1, len(vals), 2 ) ]
        self._center= Float2( xs[0], ys[0] )
        self._points= [ Float2(x, y) for x, y in zip(xs[1:], ys[1:]) ]
        # Load pices:
        self.agentsFromChildren( aPod.children() )
        return self

    def agentsFromChildren(self, aListOfPod):
        self._agents= aListOfPod
        return self

    # to str
    def str(self, name="Tile", ident=0): 
        # Myself :
        s= f"{name}-{self.number()}/{self.matter()}"
        x, y = self._center.tuple()
        x, y = round(x, 2), round(y, 2)
        s+= f" center: ({x}, {y})"
        s+= " adjs: "+ str(self._adjacencies)
        s+= f" agents({ len(self.agents()) })"
        return s
    
    def __str__(self): 
        return self.str()
    