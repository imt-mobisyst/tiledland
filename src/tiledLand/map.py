from .tile import Tile
from .joint import Joint

class Map:
    # Initialization Destruction:
    def __init__(self, diagonal= 1.0):
        # Dependancies:
        # Attributes:
        self._range= diagonal/2.0
        self._tiles= []
        self._links= []

    def setTags( self, tags ):
        self._tags= tags
    
    # Accessors:
    def size(self):
        return len(self._tiles)

    def tiles(self):
        return self._tiles
    
    def tile(self, tileId):
        return self._tiles[tileId-1]
    
    def links( self, tileId ):
        return self._links[tileId-1]

    def adjacencies(self, tileId):
        return [ t for t, gi, gt in self.links(tileId) ]

    def gateIds(self, tileId):
        return [ (gi, gt) for t, gi, gt in self.links(tileId) ]
        
    def joints(self, idA):
        tileA= self.tile(idA)
        return [  
            Joint( tileA, self.tile(idB), gateA, gateB )
            for idB, gateA, gateB in self.links( idA )
        ]

    def connexions(self):
        edges= []
        for i in range( 1, self.size()+1 ):
            for target in self.adjacencies(i) :
                if i < target :
                    edges.append( (i, target) )
        return edges

    def allJoints(self):
        joints= []
        for i in range( 1, self.size()+1 ):
            for j, gi, gj in self.links(i) :
                if i < j :
                    joints.append( Joint( self.tile(i), self.tile(j), gi, gj ) )
        return joints
    
    # Construction:
    def addTile( self, aTile ):
        self._tiles.append( aTile )
        self._links.append( [] )
        return len(self._tiles)

    def addNewTile( self, aPosition ):
        return self.addTile( self._TileGenerator(aPosition) )
    
    def connect( self, tileIdA, tileIdB):
        iA= tileIdA-1
        iB= tileIdB-1
        tileA= self._tiles[iA]
        tileB= self._tiles[iB]
        gateA= tileA.findGateSegment( tileB.center() )
        gateB= tileB.findGateSegment( tileA.center() )
        if tileIdB not in self._links[iA] :
            self._links[iA].append( (tileIdB, gateA, gateB) )
        if tileIdA not in self._links[iB] :
            self._links[iB].append( (tileIdA, gateB, gateA) )
        