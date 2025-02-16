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

    # Test:
    def isTile(self, iTile):
        return 0 < iTile and iTile <= self.size()
    
    def isEdge(self, iFrom, iTo):
        return iTo in self.tile(iFrom).adjacencies()
    
    def box(self):
        if self._size == 0 :
            return Box()
        box= self._tile[0].box()
        for t in self._tile[1:] :
            box+= t.box()
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
                        iTile, matrix[i][j],
                        Float2( dist*j, dist*(maxLine-i) ),
                        tileSize
                    )
                    self._tiles.append( tile )
                    matrix[i][j]= iTile
        self._size= iTile
        # Basic Piece Shape:
        self._shapes= [ Shape().initializeRegular( tileSize*0.7, 8 ) ]
        return self

    def clearTiles( self ):
        self._tiles= [Tile()]
        self._size= 0
        return self

    def addTile( self, aTile ):
        print( f"append: {self._size} - {aTile}" )
        self._size+= 1
        aTile.setId( self._size )
        self._tiles.append( aTile )
        print( f"tiles: {self._tiles}" )
        print( f"{self}" )

        return self._size

    #def addPiece( self, aPod, tileId, brushId=0, shapeId=0 ):
    #    tile= self.tile( tileId )
    #    tile.append( aPod, brushId, shapeId )
    #    return tile.id()
    
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
    
    # Iterator over scene tiles
    def __iter__(self):
        self._ite= 1
        return self

    def __next__(self):
        if self._ite <= self.size() :
            tile = self.tile( self._ite )
            edges= self.edgesFrom( self._ite )
            self._ite += 1
            return tile, edges
        else:
            raise StopIteration

    def iTile(self):
        return self._ite-1
    
    # string:
    def str(self, name="Scene"):
        eltStrs =[]
        print( f"> {self.tiles()}")
        for t in self.tiles() :
            eltStrs.append( f"- {t}" )
            for bod in t.bodies() :
                eltStrs.append( f"  - {bod}" )
        return f"{name}:\n" + "\n".join( eltStrs )
    
    def __str__(self):
        return self.str()