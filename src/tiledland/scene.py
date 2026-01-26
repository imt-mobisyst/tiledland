from .pod import Podable, Pod
from .geometry import Point, Box, Convex
from .tile import Tile
from .agent import Agent

import math

class Scene(Podable):

    # Constructor:
    def clear( self ):
        self._tiles= []
        self._agents= [[]]
        self._size= 0
        return self
    
    def __init__(self, shapes= [], resolution= 0.01):#, agentFactory= Agent):
        self._factory= Agent #lambda identifier, group : Agent( identifier, group, shape=Convex().initializeRegular(0.8, 5) ).setMatter(1)
        self.clear()
        for s in shapes :
            self.createTile( s )
        self._resolution= resolution
        
    # Accessor:
    def resolution(self):
        return self._resolution
    
    def size(self):
        return self._size
    
    def tiles(self):
        return self._tiles

    def tile(self, iCell):
        return self._tiles[iCell-1]

    def agent(self, iAgent, group=0 ):
        return self._agents[group][iAgent-1]

    def numberOfGroups(self):
        return len(self._agents)
    
    def numberOfAgents(self, group=0):
        if group < len(self._agents) :
            return len( self._agents[group] )
        return 0
    
    # Graph:
    def adjacencies(self, iTile) :
        return self.tile(iTile).adjacencies()
    
    def edges(self):
        edgeList= []
        for t in self.tiles() :
            edgeList+= [ (t.id(), neibor) for neibor in t.adjacencies() ]
        return edgeList

    def neighbours(self, iTile):
        neibs= [] 
        for iNei in self.adjacencies(iTile) :
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

    # Test:
    def isAgent(self, iAgent, group= 1):
        return group < len(self._agents)  and iAgent-1 < len(self._agents[group])
    
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

    def testNumberOfAgents(self):
        nb1= 0
        nb2= 0
        for t in self.tiles() :
            nb1+= t.count()
        for grp in self._agents :
            nb2+= len(grp)
        assert nb1 == nb2
        return nb1
    
    # Construction:
    def initializeLine( self, size, tileSize= 1.0, separation= 0.1, connect=True ):
        dist= tileSize+separation
        shape= Convex().initializeSquare(tileSize)
        self._tiles= [
            Tile( i+1, Point(dist*i, 0.0), shape.copy() )
            for i in range(size)
        ]
        self._size= size
        self.setResolution( separation )
        if connect :
            self.connectAllClose()
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
                        Point( dist*j, dist*(maxLine-i) ),
                        Convex().initializeSquare(tileSize),
                        matrix[i][j]
                    )
                    self._tiles.append( tile )
                    #matrix[i][j]= iTile
        
        self._size= iTile
        self.setResolution( separation )
        if connect :
            self.connectAllClose()
        return self

    def initializeHexa( self, matrix, tileSize= 1.0, separation=0.1, connect=True ):
        cosPi06= math.cos(math.pi/6)
        dist= tileSize*cosPi06 + separation
        vdist= dist*cosPi06
        hdelta= dist*0.5
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
                        Point( delta+dist*j, vdist*iLine ),
                        Convex().initializeRegular(tileSize, 6),
                        matrix[i][j]
                    )
                    self._tiles.append( tile )
                    #matrix[i][j]= iTile
        self._size= iTile
        self.setResolution( separation )
        if connect :
            self.connectAllClose()
        return self
    
    def addTile( self, aTile ):
        self._size+= 1
        aTile.setId( self._size )
        self._tiles.append( aTile )
        return self._size
    
    def createTile( self, aConvex ):
        self._size+= 1
        position= aConvex.setOnCenter()
        self._tiles.append( Tile( self._size, position, aConvex ) )
        return self._size
    
    def setResolution(self, resolution):
        self._resolution= resolution
        return self

    def setAgentFactory(self, agentFactory ):
        self._factory= agentFactory
        return self


    def clearAgents(self):
        for t in self.tiles() :
            t.clear()
        self._agents= [[]]
        return self

    def __addAgent( self, anAgent ):
        group= anAgent.group()
        while len(self._agents) <= group :
            self._agents.append([])
        assert anAgent.id() == len(self._agents[group])+1 
        self._agents[group].append(anAgent)
    
    def popAgentOn(self, iTile=1, group= 0 ):
        while len(self._agents) <= group :
            self._agents.append([])
        if iTile > self.size() :
            return False
        ag= self._factory( len(self._agents[group])+1, group )
        ag.setTile(iTile)
        ag.setPosition( self.tile(iTile).position().copy() )
        self.tile(iTile).append( ag )
        self.__addAgent(ag)
        return ag

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

    def connectAllClose(self):
        return self.connectAllDistance( 1.001*self._resolution )
    
    def connectAllDistance(self, distance):
        return self.connectAllConditions( conditionFromTo=lambda tileFrom, tileTo : tileFrom.bodyDistance( tileTo ) < distance )

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
    
    # Agent Collection:
    def allAgents( self, iGroup=0 ):
        alls= []
        for ags in self._agents:
            alls+= ags
        return alls
    
    def agents( self, iGroup=0 ):
        return self._agents[iGroup]

    def agentTiles( self, iGroup=0 ):
        return [ ag.tile() for ag in self.agents(iGroup) ]

    # Podable:
    def asPod( self, name= "Scene" ):
        return Pod().fromLists(
            [name], [], [],
            [ t.asPod() for t in self.tiles() ]
        )
    
    def fromPod( self, aPod ):
        self.clear()
        allAgents= []
        for absTile in aPod.children() :
            t= Tile().fromPod( absTile, self._factory )
            self.addTile(t)
            for ag in t.agents() :
                self.__addAgent(ag)
        return self
    
    # string:
    def str(self, name="Scene"):
        eltStrs =[]
        for t in self.tiles() :
            eltStrs.append( f"- {t}" )
            for ag in t.agents() :
                eltStrs.append( f"  - {ag}" )
        return f"{name}:\n" + "\n".join( eltStrs )
    
    def __str__(self):
        return self.str()