from .pod import Podable, Pod
from .geometry import Float2, Box, Shape
from .tile import Tile
from .body import Body

class Scene(Podable):

    # Constructor:
    def __init__(self, bodyConstructor= Body):
        self._bodyCtt= bodyConstructor
        self.clear()

    # Accessor:
    def size(self):
        return self._size
    
    def tiles(self):
        return self._tiles

    def tile(self, iCell):
        return self._tiles[iCell-1]

    def body(self, iBody):
        return self._bodies[iBody-1]

    def numberOfBodies(self):
        return len(self._bodies)

    def neighbours(self, iCell):
        neibs= [] 
        for iNei in self.tile(iCell).adjacencies() :
            dir= self.tile(iCell).clockDirection( self.tile(iNei).position() )
            neibs.append( (iNei, dir) )
        return neibs
    
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
        box= self.tile(1).box()
        for t in self.tiles()[1:] :
            box.merge( t.box() )
        return box
    
    def testNumberOfBodies(self):
        nb= 0
        for t in self.tiles() :
            nb+= t.count()
        assert nb == len(self._bodies)
        return nb
    
    # Construction:
    def append( self, tile ):
        self._tiles.append( tile )
        self._size+= 1
        self.tile( self._size ).setId( self._size )
        return self._size

    def initializeLine( self, size, shape= None, distance=1.0, connect=True ):
        if shape is None :
            shape= Shape().initializeSquare(0.9)
        self._tiles= [
            Tile( i+1, Float2(distance*i, 0.0), shape.copy() )
            for i in range(size)
        ]
        self._size= size
        return self
    
    def initializeGrid( self, matrix, tileSize= 1.0, separation=0.1, connect=True ):
        dist= tileSize+separation
        self._tiles= []
        
        iTile= 0
        maxLine= len(matrix)-1
        for i in range( len(matrix) ) :
            for j in range( len(matrix[i]) ) :
                if matrix[i][j] >= 0 : 
                    iTile+= 1
                    tile= Tile(
                        iTile,
                        Float2( dist*j, dist*(maxLine-i) ),
                        Shape().initializeSquare(tileSize),
                        matrix[i][j]
                    )
                    self._tiles.append( tile )
                    #matrix[i][j]= iTile
        self._size= iTile

        if connect :
            self.connectAllCondition(
                lambda tileFrom, tileTo :  tileFrom.centerDistance( tileTo ) < (tileSize+separation)*1.1
            )
        return self

    def setBodyConstrutor(self, bodyConstructor ):
        self._bodyCtt= bodyConstructor
        return self

    def clear( self ):
        self._tiles= []
        self._bodies= []
        self._size= 0
        return self

    def addTile( self, aTile ):
        assert aTile.bodies() == []
        self._size+= 1
        aTile.setId( self._size )
        self._tiles.append( aTile )
        return self._size

    def clearBodies(self):
        for t in self.tiles() :
            t.clear()
        self._bodies= []
        return self

    def popBodyOn(self, iTile=1 ):
        bod= self._bodyCtt( len(self._bodies)+1 )
        bod.setPosition( self.tile(iTile).position().copy() )
        self.tile(iTile).append( bod )
        self._bodies.append( bod )
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
        self.clear()
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