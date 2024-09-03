class Map:
    # Initialization Destruction:
    def __init__(self, diagonal= 1.0):
        # Dependancies:
        from . import Tile, pointlist_hexagon
        # Attributes:
        self._range= diagonal/2.0
        self._tiles= []
        self._joints= []
        self._reverces= []
        # Tools:
        self._TileGenerator= lambda position : Tile( pointlist_hexagon( position, self._range ) )

    def setTags( self, tags ):
        self._tags= tags
    
    # Accessors:addTile
    def size(self):
        return len(self._tiles)

    def tiles(self):
        return self._tiles
    
    # Construction:
    def addTile( self, aTile ):
        self._tiles.append( aTile )
        self._joints.append( [] )
        self._reverces.append( [] )
        return len(self._tiles)-1

    def addNewTile( self, aPosition ):
        return self.addTile( self._TileGenerator(aPosition) )
    
    #def connect( self, aTileId1, aTileId2 ):
