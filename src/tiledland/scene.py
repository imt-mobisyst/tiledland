from .pod import Podable, Pod
from .geometry import Float2, Box, Shape
from .tile import Tile
from .body import Body

class Scene(Podable):

    # Constructor:
    def __init__( self, bodyConstructor= Body ):
        self._bodyCtt= bodyConstructor
        self._tiles= []
        self._size= 0

    # Accessor:
    def size(self):
        return self._size
    
    def tiles(self):
        return self._tiles[1:]

    def tile(self, iCell):
        return self._tiles[iCell]

    def edges(self):
        edgeList= []
        for t in self.tiles() :
            edgeList+= [ (t.id(), neibor) for neibor in t.adjacencies() ]
        return edgeList

    def countBodies(self):
        nb= 0
        for t in self.tiles() :
            nb+= t.count()
        return nb

    # Test:
    def isTile(self, iTile):
        return 0 < iTile and iTile <= self.size()
    
    def isEdge(self, iFrom, iTo):
        return iTo in self.tile(iFrom).adjacencies()
    
    def box(self):
        if self._size == 0 :
            return Box()
        box= self.tile(1).box()
        for t in self.tiles()[1:] :
            box.merge( t.box() )
        return box

    # Construction:
    def initializeLine( self, size, shape=Shape(0.9), distance=1.0 ):
        self._tiles= [None] + [
            Tile( i+1, Float2(distance*i, 0.0), shape.copy() )
            for i in range(size)
        ]
        self._size= size
        return self
    
    def initializeGrid( self, matrix, tileSize= 1.0, separation=0.1 ):
        dist= tileSize+separation
        self._tiles= [None]
        
        iTile= 0
        maxLine= len(matrix)-1
        for i in range( len(matrix) ) :
            for j in range( len(matrix[i]) ) :
                if matrix[i][j] >= 0 : 
                    iTile+= 1
                    tile= Tile(
                        iTile,
                        Float2( dist*j, dist*(maxLine-i) ),
                        Shape(tileSize),
                        matrix[i][j]
                    )
                    self._tiles.append( tile )
                    matrix[i][j]= iTile
        self._size= iTile
        # Basic Piece Shape:
        self._shapes= [ Shape().initializeRegular( tileSize*0.7, 8 ) ]
        return self

    def clearTiles( self ):
        self._tiles= [None]
        self._size= 0
        return self

    def addTile( self, aTile ):
        self._size+= 1
        aTile.setId( self._size )
        self._tiles.append( aTile )
        return self._size

    def clearBodies(self):
        for t in self.tiles() :
            t.clear()
        return self


    def popBodyOn(self, iTile=1 ):
        bod= self._bodyCtt()
        bod.setPosition( self.tile(iTile).position().copy() )
        self.tile(iTile).append( bod )
        return bod

    def connect(self, iFrom, iTo):
        self.tile(iFrom).connect(iTo)
        return self

    def connectAll(self, aList):
        for anElt in aList :
            self.connect( anElt[0], anElt[1] )

    def connectAllCondition(self, conditionFromTo=lambda tfrom, tto : True, conditionFrom=lambda tfrom : True ):
        size= self.size()
        for i in range(1, size+1) :
            tili= self.tile(i)
            if conditionFrom( tili ) :
                for j in range(1, size+1) :
                    tilj= self.tile(j)
                    if conditionFromTo( tili, tilj ): # :
                       self.connect( i, j )

    # Podable:
    def asPod( self ):
        return Pod().fromLists(
            ["Scene"], [], [],
            [ t.asPod() for t in self.tiles() ]
        )
    
    def fromPod( self, aPod ):
        self.clearTiles()
        for absTile in aPod.children() :
            self.addTile( Tile().fromPod( absTile, self._bodyCtt ) )
        return self
        
    # string:
    def str(self, name="Scene"):
        eltStrs =[]
        for t in self.tiles() :
            eltStrs.append( f"- {t}" )
            for bod in t.bodies() :
                eltStrs.append( f"  - {bod}" )
        return f"{name}:\n" + "\n".join( eltStrs )
    
    def __str__(self):
        return self.str()