
from .carrier import Carrier
from ... import Float2, Shape, Box, scene, Tile, artist
import hacka as hk
import random

class Mission:
    def __init__( self, start= 0, final= 0, reward= 0, owner= 0 ):
        self.start= start
        self.final= final
        self.reward= reward
        self.owner= owner

    def fromList(self, aList):
        self.start= aList[0]
        self.final= aList[1]
        self.reward= aList[2]
        self.owner= aList[3]
        return self

    def asList(self):
        return [self.start, self.final, self.reward, self.owner]
    
    def asTuple(self):
        return self.start, self.final, self.reward, self.owner

class World( scene.Scene ):
    def __init__(self, name="Pick'nDel", numberOfPlayers= 1):
        super().__init__()
        self.setAgentFactory(Carrier)
        self._name= name
        self._missions= []
        self._encumbers= []
        # Initialize Artist :
        self._artist= artist.Artist().initializePNG( "shot-pickndel.png" )
        self._artist.flip()
        self._artist.fitBox( Box([Float2(-0.5, -0.5), Float2(9.5, 6.5)] ), 10 )
        #self._artist.fitBox( self.box(), 10 )
        self.marketBrush= self._artist._panel[6]
        self.marketBrush.width= 8

    # Accessor: 
    def name(self):
        return self._name
    
    def carrierTile(self, iCarrier= 1, iPlayer= 1):
        return self.agent(iCarrier, iPlayer).tile()
    
    def carrierMission(self, iCarrier= 1, iPlayer= 1):
        mission= self.agent(iCarrier, iPlayer).mission()
        if mission != 0 : 
            return mission
        return self.missionIndexes()[0]

    def carrierGoal(self, iCarrier= 1, iPlayer= 1):
        mission= self.agent(iCarrier, iPlayer).mission()
        if mission != 0 : 
            return self.mission( mission ).final
        mission= self.missionIndexes()[0]
        return self.mission( mission ).start
    
    def missions(self):
        return self._missions

    def isMission(self, iMission):
        return ( 0 < iMission and iMission <= len(self._missions) )

    def mission(self, index):
        return self._missions[index-1]
    
    def missionIndexes(self):
        l= []
        i= 1
        for m in self._missions :
            if m.start > 0 :
                l.append(i)
            i+= 1
        return l
    
    def carrierTiles(self, iPlayer):
        return [ m.tile() for m in self.agents(iPlayer) ]
    
    def encumber(self, iTile):
        return self._encumbers[iTile-1]

    # Construction:
    def initializeMoves(self):
        for group in range( self.numberOfGroups() ) :
            for car in self.agents(group) :
                car.setMove(0)

    def append( self, tile, encumber= 0.0 ):
        super(World, self).append(tile)
        self._encumbers.append(encumber)

    def setEncumber( self, iTile, value ):
        self._encumbers[iTile-1]= value
        return self

    def resetEncumbers( self, defaultValue= 0.0 ):
        self._encumbers= [ defaultValue for i in range(self.size()) ]
        return self
    
    def initializeLine( self, size, shape= None, distance=1.0, connect=True ):
        super(World, self).initializeLine(size, shape, distance, connect)
        self.resetEncumbers()
        return self
    
    def initializeGrid( self, matrix, tileSize= 1.0, separation=0.1, encumbers= [[],[]], connect=True ):
        super(World, self).initializeGrid(matrix, tileSize, separation, connect)
        self.resetEncumbers()
        for iTile, enc in zip( encumbers[0], encumbers[1] ) :
            self.setEncumber( iTile, enc )
        return self

    def clear( self ):
        super(World, self).clear()
        self._encumbers= []

    def addTile( self, aTile, encumber= 0.0 ):
        super(World, self).addTile(aTile)
        self._encumbers.append(encumber)
        return self._size

    # Mission :
    def setMissions( self, aListOfTuples, pay= 124 ):
        self._missions= [
            Mission(iFrom, iTo, pay, 0)
            for iFrom, iTo in aListOfTuples 
        ]
    
    def clearMissions(self):
        self._missions= []
        for group in range(self.numberOfGroups()+1) :
            for iCarrier in range(1, self.numberOfAgents(group)+1) :
                self.agent( iCarrier, group ).setMission(0)
        return self

    def addMission( self, iFrom, iTo, pay= 124 ):
        self._missions.append( Mission(iFrom, iTo, pay, 0) )
        return len(self._missions)
    
    def addMissionAtRandom( self ):
        tileIndexes= range( 1, self.size()+1 )
        return self.addMission( random.choice( tileIndexes ), random.choice(tileIndexes) )

    def updateMission(self, iMission, iFrom, iTo, pay, owner):
        self._missions[iMission-1]= Mission(iFrom, iTo, pay, owner)

    def addRandomMission(self):
        bound= self._engine._map.size()+1
        iFrom= random.randrange(1, bound)
        iTo= random.randrange(1, bound)
        pay= 10+random.randrange(bound)
        self._engine.addMission( iFrom, iTo, pay )
        return iFrom, iTo, pay

    # Moving:
    def move(self, iFrom, clockDir):
        #print( f">>> move {iFrom}, {clockDir} ({self.encumber(iFrom)})" )
        if self.tile(iFrom).count() == 0 or clockDir == 0 :
            return iFrom
        if random.random() < self.encumber(iFrom) :
            return iFrom
        iTo= self.clockposition( iFrom, clockDir ) 
        return self.teleport(iFrom, iTo)

    def teleport( self, iFrom, iTo ):
        if self.tile(iFrom).count() == 0 or self.tile(iTo).count() :
            return False
        # move:
        # Get from iFrom
        carrier= self.tile(iFrom).agent()
        self.tile(iFrom).clear()

        # Set on iTo
        self.tile(iTo).append(carrier)
        carrier.setTile( iTo )
        carrier.setPosition( self.tile(iTo).position() )
        return iTo
    
    # Podable:
    def asPod( self ):
        return hk.Pod( self._name, [], [], [ super(World, self).asPod(), self.missionsAsPod() ] )
    
    def missionsAsPod(self):
        missionPod= hk.Pod( "Missions" )
        for m in self._missions :
            missionPod.append( hk.Pod( "Mission", m.asList() ) )
        return missionPod
    
    def carriersAsPod(self):
        podMobiles= hk.Pod( "Carriers" )
        for group in range( self.numberOfGroups() ):
            for car in self.agents( group ):
                mPod= hk.Pod( "carrier", [group, car.id(), car.tile(), car.mission()] )
                podMobiles.append(mPod)
        return podMobiles

    def fromPod( self, aPod ):
        self._name= aPod.label()
        super(World, self).fromPod( aPod.child(1) )
        self.missionsFromPod(  aPod.child(2) )
        return self
    
    def missionsFromPod(self, aPod):
        self._missions= []
        for childPod in aPod.children() :
            self._missions.append( Mission().fromList( childPod.integers() ) )
        return self._missions
    
    def carriersFromPod(self, aPod):
        self.clearAgents()
        for pod in aPod.children() :
            iPlayer= pod.integer(1)
            iCarrier= pod.integer(2)
            pos= pod.integer(3)
            mis= pod.integer(4)
            carrier= self.popAgentOn( pos, iPlayer )
            assert carrier.id() == iCarrier
            carrier.setMission(mis)
        return self._agents

    def setOnPodState(self, aPod):
        self.missionsFromPod( aPod.child(1) )
        self.carriersFromPod( aPod.child(2) )
        return aPod.integer(1)
    
    # Rendering :
    def render(self):
        self._artist.drawScene( self )
        # Market:
        self._artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            self.marketBrush
        )
        self._artist._fontSize= 20
        self._artist.write( 6.6, 2.2, "Market Place:", self.marketBrush )
        self._artist._fontSize= 16
        sep= 0.0
        for i in self.missionIndexes() :
            mFrom, mTo, pay, iPlayer= self.mission(i).asTuple()
            self._artist.write( 6.8, 1.9-sep, f".{i}", self.marketBrush) 
            self._artist.write( 7.2, 1.9-sep, f"- {mFrom} to: {mTo}", self.marketBrush )
            if iPlayer == 0 :
                self._artist.write( 8.5, 1.9-sep, f"({pay} ¢)", self.marketBrush )
            else :
                self._artist.write( 8.4, 1.9-sep, f"(Team-{iPlayer})", self.marketBrush )
            sep+= 0.24
        # Finalize:
        self._artist.flip()

