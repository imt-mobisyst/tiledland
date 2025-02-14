from hacka.py import pod
from .shape import Float2, Shape
from .tile import Tile

class Map( pod.PodInterface ):

    # Constructor:
    def __init__( self ):
        self._tiles= []
        self._size= 0
        self._shapes= []

    # Accessor:
    def size(self):
        return self._size

    def isTile(self, iTile):
        return 0 < iTile and iTile <= self.size()
    
    def tiles(self):
        return self._tiles[1:]

    def tile(self, iCell):
        return self._tiles[iCell]

    def edges(self):
        edgeList= []
        for t in self.tiles() :
            edgeList+= [ (t.number(), neibor) for neibor in t.adjacencies() ]
        return edgeList

    def isEdge(self, iFrom, iTo):
        return iTo in self.tile(iFrom).adjacencies()
    
    def box(self):
        if self.size() == 0 :
            return [ (0.0, 0.0), (0.0, 0.0) ]
        tiles= self.tiles()
        minPoint, maxPoint= tiles[0].box()
        for t in tiles[1:] :
            tMin, tMax= t.box()
            if tMin.x() < minPoint.x():
                minPoint.setx( tMin.x() )
            if tMin.y() < minPoint.y():
                minPoint.sety( tMin.y() )
            if tMax.x() > maxPoint.x():
                maxPoint.setx( tMax.x() )
            if tMax.y() > maxPoint.y():
                maxPoint.sety( tMax.y() )

        return [minPoint, maxPoint]

    def shapes(self):
        return self._shapes
        
    def shape(self, i=0):
        return self._shapes[i]
    
    # Construction:
    def initializeLine( self, size, tileSize=0.9, separation=0.1 ):
        dist= tileSize+separation
        self._tiles= [None] + [
            Tile(i+1, 0, Float2(dist*i, 0.0), tileSize )
            for i in range(size)
        ]
        self._size= size
        # Basic Piece Shape:
        self._shapes= [ Shape().setShapeRegular( tileSize*0.6, 8 ) ]
        return self
    
    def initializeSquares( self, matrix, tileSize= 1.0, separation=0.1 ):
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
        self._shapes= [ Shape().setShapeRegular( tileSize*0.7, 8 ) ]
        return self

    def addTile( self, aTile ):
        self._size+= 1
        aTile.setNumber( self._size )
        self._tiles.append( aTile )
        return self._size

    def addShape( self, aShape ):
        self._shapes.append( aShape )
        return len(self._shapes)

    def addPiece( self, aPod, tileId, brushId=0, shapeId=0 ):
        tile= self.tile( tileId )
        tile.append( aPod, brushId, shapeId )
        return tile.number()
    
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

    # Pod interface:
    def asPod(self, family= "Map"):
        bPod= pod.Pod( family )
        for s in self.shapes() :
            bPod.append( s.asPod() )
        for t in self.tiles() :
            bPod.append( t.asPod() )
        return bPod
    
    def fromPod(self, aPod):
        self._tiles= [None]
        self._shapes= []
        self._size= 0
        kids= aPod.children()
        for kid in kids :
            if kid.family() == "Shape" :
                self.addShape( Shape().fromPod( kid ) )
            if kid.family() == "Tile" :
                self.addTile( Tile().fromPod( kid ) )
        return self

    # Iterator over map cells
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
    def str(self, name="Map"):
        eltStrs =[]
        for s in self.shapes() :
            eltStrs.append( f"- {s}" )
        for t in self.tiles() :
            eltStrs.append( f"- {t}" )
            for piece in t.pieces() :
                eltStrs.append( f"  - {piece}" )
        return f"{name}:\n" + "\n".join( eltStrs )
    
    def __str__(self): 
        return self.str()