from .pod import Podable, Pod
from .geometry import Float2, Box, Shape
from .tile import Tile
from .agent import Agent

class Scene(Podable):

    # Constructor:
    def __init__(self, agentFactory= Agent):
        self._factory= agentFactory
        self.clear()

    # Accessor:
    def size(self):
        return self._size
    
    def tiles(self):
        return self._tiles

    def tile(self, iCell):
        return self._tiles[iCell-1]

    def agent(self, iAgent, iOwner=0 ):
        return self._agents[iOwner][iAgent-1]

    def numberOfOwner(self):
        return len(self._agents)
    
    def numberOfAgent(self, iOwner):
        return len( self._agents[iOwner] )

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

    def setAgentFactory(self, agentFactory ):
        self._factory= agentFactory
        return self

    def clear( self ):
        self._tiles= []
        self._agents= [[]]
        self._size= 0
        return self

    def addTile( self, aTile ):
        assert aTile.agents() == []
        self._size+= 1
        aTile.setId( self._size )
        self._tiles.append( aTile )
        return self._size

    def clearAgents(self):
        for t in self.tiles() :
            t.clear()
        self._agents= [[]]
        return self

    def popAgentOn(self, iTile=1, owner= 0 ):
        if iTile > self.size() :
            return False
        while len(self._agents) <= owner :
            self._agents.append([])
        ag= self._factory( len(self._agents[owner])+1, owner )
        ag.setTile(iTile)
        ag.setPosition( self.tile(iTile).position().copy() )
        self.tile(iTile).append( ag )
        self._agents[owner].append( ag )
        return ag

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

    # Agent accessors:
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
    def asPod( self ):
        return Pod().fromLists(
            ["Scene"], [], [],
            [ t.asPod() for t in self.tiles() ]
        )
    
    def fromPod( self, aPod ):
        self.clear()
        for absTile in aPod.children() :
            self.addTile( Tile().fromPod( absTile, self._factory ) )
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