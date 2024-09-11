import math

from .tile import Tile
from .joint import Joint
from .geometry import Coord2

class Map:
    # Initialization Destruction:
    def __init__(self, tileCenters= [], edges= [], tileModel= Tile() ):
        # Dependancies:
        # Attributes:
        self._tiles= [ tileModel.copy().moveTo( coord ) for coord in tileCenters ]
        self._links= [ [] for coord in tileCenters ]
        for a, b in edges :
            self.connect( a, b )

    def setTags( self, tags ):
        self._tags= tags
    
    # Construction:
    def addTile( self, aTile ):
        self._tiles.append( aTile )
        self._links.append( [] )
        return len(self._tiles)
    
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
    
    # Generator:
    def setSquareGrid( self, matrix, origine= Coord2(), scale= 1.0 ):
        matrix.reverse()
        demi= scale*0.5
        lenght= scale*0.9
        # Create tiles :
        y= origine.y() + demi
        for iLine in range( len( matrix ) ) :  
            x= origine.x() + demi
            for iCell in range( len( matrix[iLine] ) ) :
                if matrix[iLine][iCell] > 0 :
                    tileId= self.addTile( Tile().setSquare( Coord2(x, y), lenght ) )
                    # Test Bottom:
                    if iLine > 0 and matrix[iLine-1][iCell] != 0 :
                        self.connect( matrix[iLine-1][iCell], tileId )
                    # Test Left:
                    if iCell > 0 and matrix[iLine][iCell-1] != 0 :
                        self.connect( matrix[iLine][iCell-1], tileId )
                    # record the new tileId.
                    matrix[iLine][iCell]= tileId
                # Increment
                x+= scale
            # Increment
            y+= scale
        
        return self
    
    def setHexaGrid( self, matrix, origine= Coord2(), scale= 1.0 ):
        matrix.reverse()
        demi= scale*0.5
        stepX= scale
        stepY= math.sin(math.pi/3) * scale
        nbCell= len( matrix[0])
        # Create tiles :
        y= origine.y() + demi
        for iLine in range( len( matrix ) ) :  
            x= origine.x() + demi
            if iLine%2 == 1 :
                x+= demi
            assert( nbCell == len( matrix[iLine] ) )
            for iCell in range( len( matrix[iLine] ) ) :
                if matrix[iLine][iCell] > 0 :
                    # Create a new Tile
                    tileId= self.addTile( Tile().setRegular( 6, Coord2(x, y), scale ) )
                    # Test & connect Bottom 2.0:
                    if iLine%2 == 0 :
                        if iLine > 0 and iCell > 0 and matrix[iLine-1][iCell-1] != 0 :
                            self.connect( matrix[iLine-1][iCell-1], tileId )
                    # Test & connect Bottom 1:
                    if iLine > 0 and matrix[iLine-1][iCell] != 0 :
                        self.connect( matrix[iLine-1][iCell], tileId )
                    # Test & connect Bottom 2.1:
                    if iLine%2 == 1 :
                        if iLine > 0 and iCell < (nbCell-1) and matrix[iLine-1][iCell+1] != 0 :
                            self.connect( matrix[iLine-1][iCell+1], tileId )
                    # Test & connect Left:
                    if iCell > 0 and matrix[iLine][iCell-1] != 0 :
                        self.connect( matrix[iLine][iCell-1], tileId )
                    # record the new tileId.
                    matrix[iLine][iCell]= tileId
                # Increment
                x+= stepX
            # Increment
            y+= stepY
        
        return self