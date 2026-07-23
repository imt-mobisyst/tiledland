import hacka
from .geometry import Point, Box, Convex
from .entity import AbsEntity, Entity
from .tile import Tile

import math

class Map(AbsEntity):
    defaultEntity= Entity()

    def __init__(self, epsilon= 0.01):
        assert( type(epsilon) == float )
        super().__init__()
        self._tiles= []
        self._size= 0
        self._epsilon= epsilon

    # Initialization:
    def clear( self ):
        self._tiles= []
        self._size= 0
        return self

    def fromShapes(self, shapes, group=0):
        # Clean basis:
        self.clear()
        for s in shapes :
            self.createTile(s, group)
        return self
    
    def fromGridRectangles(self, aGrid, tileSize= 1.0):
        self.clear()
        self._epsilon= aGrid.resolution() * 0.4

        # Foreach value possibility:
        minVal, maxVal= aGrid.valueMinMax()
        i= 0
        for pixval in range( minVal, maxVal+1 ):
            # Add all shapes
            shapes= aGrid.makeRectangles(pixval, tileSize)
            for s in shapes :
                i+= 1
                assert self.createTile(s, pixval) == i
        
        # Connect all elements:
        self.connectAllClose( aGrid.resolution() )

        # Optimize the definition:
        for factor in [0.2, 0.4, 0.6, 0.8] :
            self.mergeAllPossible( aGrid.resolution() * factor, tileSize)

        return self
    
    def fromGridConvexes(self, aGrid, tileSize=1.0, minSizeRatio=0.1, pixelValues= False):
        self.clear()
        seam= aGrid.resolution() * 1.001
        self._epsilon= aGrid.resolution() * 0.001
        gridConvexRadius= max(2, round( (tileSize/seam)/2.0 ))
        assert( 0.0 <= minSizeRatio and minSizeRatio <= 1.0)
        minSize= tileSize*minSizeRatio

        if not pixelValues :
            minVal, maxVal= aGrid.valueMinMax()
            pixelValues= range(minVal, maxVal+1)
        
        # Foreach value possibility:
        for pixval in pixelValues :
            convexes= aGrid.makeConvexes(pixval, gridConvexRadius, minSize)
            for conv in convexes :
                self.createTile(conv, pixval)

        # Connect all elements:
        self.connectAllClose( seam )

        return self

    def initLine( self, size, tileSize= 1.0, separation= 0.1, connect=True ):
        dist= tileSize+separation
        shape= Convex().initSquare(tileSize)
        self._tiles= [
            Tile( i+1, 0, shape, Point(dist*i, 0.0) )
            for i in range(size)
        ]
        self._size= size
        if connect :
            self.connectAllClose(1.1*separation)
        return self
    
    def initGrid( self, matrix, tileSize= 1.0, separation=0.1, connect=True ):
        dist= tileSize+separation
        shape= Convex().initSquare(tileSize)
        self._tiles= []
        
        iTile= 0
        maxLine= len(matrix)-1
        for i in range( len(matrix) ) :
            for j in range( len(matrix[i]) ) :
                if matrix[i][j] >= 0 : 
                    iTile+= 1
                    tile= Tile(
                        iTile,
                        matrix[i][j],
                        shape,
                        Point(dist*j, dist*(maxLine-i))
                    )
                    self._tiles.append( tile )
        
        self._size= iTile
        if connect :
            self.connectAllClose(1.1*separation)
        return self

    def initHexa( self, matrix, tileSize= 1.0, separation=0.1, connect=True ):
        cosPi06= math.cos(math.pi/6)
        dist= tileSize*cosPi06 + separation
        vdist= dist*cosPi06
        hdelta= dist*0.5
        shape= Convex().initRegular(tileSize, 6)
        self._tiles= []
        
        iTile= 0
        maxLine= len(matrix)-1
        for i in range( len(matrix) ) :
            for j in range( len(matrix[i]) ) :
                if matrix[i][j] >= 0 : 
                    iTile+= 1
                    iLine= maxLine-i
                    delta= (iLine%2) * hdelta
                    tile= Tile(
                        iTile,
                        matrix[i][j],
                        shape
                    )
                    tile.setPosition(delta+dist*j, vdist*iLine )
                    self._tiles.append( tile )
                    #matrix[i][j]= iTile
        self._size= iTile
        if connect :
            self.connectAllClose(1.1*separation)
        return self

    # Accessor:
    def epsilon(self):
        return self._epsilon
    
    def size(self):
        return self._size
    
    def tiles(self):
        return self._tiles

    def tile(self, iTile):
        return self._tiles[iTile-1]

    def eEentity(self, iTile, index):
        return self.tile(iTile).entity(index)

    def numberOfTiles(self):
        return self._size
    
    def numberOfEntities(self):
        c= 0
        for t in self._tiles :
            c+= len( t.entities() )
        return c

    # Graph:
    def adjacencies(self, iTile) :
        return self.tile(iTile).adjacencies()
    
    def edges(self):
        edgeList= []
        for t in self.tiles() :
            edgeList+= [ (t.index(), neibor) for neibor in t.adjacencies() ]
        return edgeList

    def neighbours(self, iTile):
        neibs= [] 
        for iNei in self.adjacencies(iTile) :
            print(f"{iTile} and {iNei}")
            clockdir= self.tile(iTile).clockDirection( self.tile(iNei).position() )
            neibs.append( (iNei, clockdir) )
        return neibs
        
    def directions(self, iTile) : 
        cx, cy= self.tile(iTile).position().asTuple()
        neibor= self.adjacencies(iTile)
        positions= [ self.tile(i).position().asTuple() for i in neibor ]
        return [ (x-cx, y-cy) for x, y in positions ]
    
    def clockBearing(self, iTile):
        clock= [
            [ 0,  9,  0],
            [ 6,  0, 12],
            [ 0,  3,  0]
        ]
        positions= [ (int(round(x, 0)), int(round(y, 0))) for x, y in self.directions(iTile) ]
        return [ clock[1+x][1+y] for x, y in positions ]

    def completeClock(self, iTile):
        clock= [ iTile for i in range(13) ]
        for it, ic in self.neighbours(iTile) :
            clock[ic]= it
        return clock

    def clockposition(self, iTile, clockDir):
        return self.completeClock(iTile)[clockDir]

    # Construction:
    def setEpsilon(self, epsilon):
        self._epsilon= epsilon
        return self

    def appendTile( self, aTile ):
        self._size+= 1
        aTile.setIndex( self._size )
        self._tiles.append( aTile )
        return aTile
    
    def createSeveralTiles(self, convexes, group):
        for c in convexes :
            self.createTile( c, group )
        
    def createTile( self, aTileShape, group= 0 ):
        aShape= aTileShape.copy()
        x, y= aShape.setOnCenter().asTuple()
        tile= Tile( 0, group, aShape )
        tile.setPosition(x, y)
        self.appendTile(tile)
        return self._size
    
    def removeTile( self, iTile ):
        for t in self._tiles :
            if t.isConnecting(iTile) :
                t.disconnect(iTile)
        for jTile in range( iTile+1, self.size()+1 ) :
            self.changeTileIndex( jTile, jTile-1 )
        self._tiles.pop(iTile-1)
        self._size-=1
        return self

    def changeTileIndex( self, iTile, newID ):
        # Change connection :
        for t in self._tiles :
            if t.isConnecting(iTile) :
                t.disconnect(iTile)
                t.connect(newID)
        # Change iTile :
        self.tile(iTile).setIndex(newID)
        return self

    # Test:
    def isTile(self, iTile):
        return 0 < iTile and iTile <= self.size()
    
    def isEdge(self, iFrom, iTo):
        return iTo in self.tile(iFrom).adjacencies()

    # Population:
    def isEntity(self, iTile, index):
        return (self.isTile(iTile) 
            and 0 < index 
            and index <= len( self.tile(iTile).entities() )
        )

    def clearEntities(self):
        for t in self.tiles() :
            t.clear()
        return self

    def tileAppendEntity( self, iTile, anEntity= None ):
        if anEntity is None :
            anEntity= type(self).defaultEntity.copy()
        tile= self.tile(iTile)
        tile.appendCenter(anEntity)
        anEntity.setPose(tile.position(), anEntity.orientation())
        return anEntity

    def tileRemoveEntity( self, iTile, iEntity ):
        anEntity= None
        if self.isEntity(iTile, iEntity) :
            anEntity= self.tile(iTile).remove(iEntity)
            anEntity.setLocation(0, 0)
        return anEntity

    def moveEntity( self, iTile, iEntity, tTile ):
        anEntity= self.tileRemoveEntity(iTile, iEntity)
        if anEntity is None :
            return anEntity
        self.tileAppendEntity(tTile, anEntity)
        return anEntity

    def connect(self, iFrom, iTo):
        self.tile(iFrom).connect(iTo)
        return self

    def connectAll(self, aList):
        for anElt in aList :
            self.connect( anElt[0], anElt[1] )

    def connectAllConditions(self, conditionFrom=lambda tfrom : True, conditionFromTo=lambda tfrom, tto : True, ):
        size= self.size()
        count= 0
        for i in range(1, size+1) :
            tili= self.tile(i)
            if conditionFrom( tili ) :
                for j in range(1, size+1) :
                    tilj= self.tile(j)
                    if conditionFromTo( tili, tilj ): # :
                       self.connect( i, j )
                       count+= 1
        return count

    def connectAllClose(self, distance):
        return self.connectAllConditions(
            conditionFromTo=lambda tileFrom, tileTo : tileFrom != tileTo and tileFrom.bodyDistance( tileTo ) < distance )

    # Distance :
    def computeDistances(self):
        s= self.size()
        self._distances= [ [ i for i in range(s+1) ] ]
        for i in range( 1, s+1 ) :
            dist= self.computeDistancesTo(i)
            self._distances.append( dist )

    def computeDistancesTo(self, iTile):
        # Initialize distances to 0:
        dists= [iTile] +  [0 for i in range( self.size() )]
        # Initialize step from iTile:
        ringNodes= self.adjacencies(iTile)
        ringDistance= 1
        # while theire is nodes to visit
        while len(ringNodes) > 0 :
            nextNodes= []
            # Visit all step nodes:
            for node in ringNodes :
                # Update distance information
                dists[node]= ringDistance
            for node in ringNodes :
                # Search for new tile to visit:
                neighbours= self.adjacencies(node)
                for candidate in neighbours :
                    if dists[candidate] == 0 :
                         nextNodes.append(candidate)
            # swith to the next step.
            ringNodes= nextNodes
            ringDistance+= 1
        # Correct 0 distance:
        dists[iTile]= 0
        return dists
    # Tile selection : 
    def selectId(self, tileCondition):
        selection= []
        for i in range(1, self.size()+1):
            if tileCondition( self.tile(i) ) :
                selection.append(i)
        return selection
    
    def selectIdSmallbox(self, maxSize):
        selection= []
        for i in range(1, self.size()+1):
            t= self.tile(i)
            tb= t.box()
            if (tb.width() < maxSize or tb.height() < maxSize) :
                selection.append(i)
        return selection
        
    # Tile Operation :
    def mergeTilesIfPossible(self, iTile1, iTile2, maxError, maxSize):
        if iTile1 == iTile2 :
            return False
        if iTile2 < iTile1 :
            return self.mergeTilesIfPossible(iTile2, iTile1, maxError, maxSize)

        tile= self.tile(iTile1)
        newConvex= tile.projectedShape().copy()
        convex2= self.tile(iTile2).projectedShape()
        removed= newConvex.merge( convex2 )
        w, h= newConvex.box().dimention()
        if w > maxSize or h > maxSize :
            return False

        # Merge ok ?
        for p in removed :
            if newConvex.distancePoint(p) > maxError :
                return False
        
        # Do merge:
        newConvex.simplify( self.epsilon() )
        tile.setProjectedShape(newConvex)
        deadTile= self.tile(iTile2)
        # merge all entities
        for ag in deadTile.entities() :
            tile.append( ag )
        
        # merge connections
        adjs= deadTile.adjacencies()
        adjs.remove(iTile1)
        tile.connectAll( adjs )
        for t in self._tiles :
            if t != self.tile(iTile1) and t.isConnecting(iTile2) :
                t.connect(iTile1)
        
        self.removeTile(iTile2)
        return True
    
    def mergeTile(self, iTile, maxError, maxSize):
        t= self.tile(iTile)
        tb= t.box()
        neighborhood= [ (i, (tb + self.tile(i).box()).score() ) for i in t.adjacencies() ]
        neighborhood.sort(key=lambda tup: tup[1])
        for neighbor, val in neighborhood :
            if ( self.tile(neighbor).group() == t.group()
                and self.mergeTilesIfPossible( neighbor, iTile, maxError, maxSize )
            ) :
                return True
        return False

    def mergeAllPossible(self, maxError= False, exepectedSize= False):
        if not maxError :
            maxError= self.epsilon()
        if not exepectedSize :
            w, h= self.box().dimention()
            exepectedSize= max(w, h)
        notok= True
        count= 0
        minSize= exepectedSize*0.5
        maxSize= exepectedSize*1.5
        while notok :
            notok= False
            for iTile in self.selectIdSmallbox(minSize) :
                if self.mergeTile(iTile, maxError, maxSize) :
                    count+= 1
                    notok= True
                    break
        
        return count

    # AbsEntity:
    def box(self):
        if self._size == 0 :
            return Box()
        box= self.tile(1).box()
        for t in self.tiles()[1:] :
            box.merge( t.box() )
        return box
    
    # Artist drawing:
    def renderNetworkOn( self, artist ):
        for tile in self.tiles() :
            cx, cy= tile.position().asTuple()
            artist.tracePoint( cx, cy, tile.brush() )
        for fromId, toId in self.edges() :
            fromX, fromY= self.tile( fromId ).position().asTuple()
            toX, toY= self.tile( toId ).position().asTuple()
            artist.traceLine( fromX, fromY, toX, toY, self.tile(fromId).brush() )
        return self

    def renderTilesOn( self, artist):
        for tile in self.tiles() :
            tile.renderOn( artist )
        for tile in self.tiles() :
            tile.writeOn( artist )
        return self
    
    def renderEntitiesOn( self, artist ):
        for tile in self.tiles() :
            x, y= tile.position().asTuple()
            position= (x+0.1, y+0.1)
            for entity in tile.entities() :
                entity.renderOn( artist )
        return self

    def renderOn( self, artist ):
        self.renderNetworkOn(artist)
        self.renderTilesOn(artist)
        self.renderEntitiesOn(artist)
        return self

    # Hacka.DataTree interface:
    def asDataTree( self, name= "Map" ):
        return hacka.DataTree(name, [], [self._epsilon],
            [ t.asDataTree() for t in self.tiles() ]
        )
    
    def fromDataTree( self, aDataTree ):
        self.clear()
        self._epsilon= aDataTree.value(1)
        allEntities= []
        for absTile in aDataTree.children() :
            t= Tile().fromDataTree( absTile )
            assert( t.index() == self.numberOfTiles()+1 )
            self.appendTile(t)
        return self

    # string:
    def str(self, name="Map"):
        eltStrs =[]
        for t in self.tiles() :
            eltStrs.append( f"- {t}" )
            for ag in t.entities() :
                eltStrs.append( f"  - {ag}" )
        return f"{name}:\n" + "\n".join( eltStrs )
    
    def __str__(self):
        return self.str()

