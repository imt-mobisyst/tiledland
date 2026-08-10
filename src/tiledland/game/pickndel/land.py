import random, hacka

import tiledland as tll
from tiledland.geometry import Point, Convex, Box

from .carrier import Carrier

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

class Land(tll.Land):
    def __init__(self, name= "Pick'n-Del", tabletop= None, nbOfActors= 14):
        super(Land, self).__init__(
            tabletop,
            bankOfEntities= [
                Carrier(i, name=n)
                for i, n in zip(range(0, nbOfActors+1), ["-"] + [ chr( ord('A') + i%26 ) for i in range(nbOfActors) ])
            ]
        )
        self._missions= []
        self._encumbers= []
        self._name= name
        
        # Initialize Artist :
        #artist= artist.createArtistPNG( "shot-pickndel.png", 800, 600 )
        #artist.flip()
        #artist.fitBox( Box([Point(-0.5, -0.5), Point(9.5, 6.5)] ), 10 )
        #artist.fitBox( self.box(), 10 )

    # Accessor: 
    def name(self):
        return self._name
    
    def carrierTile(self, iCarrier= 1, iPlayer= 1):
        return self.entity(iCarrier, iPlayer).tile()
    
    def carrierMission(self, iCarrier= 1, iPlayer= 1):
        mission= self.entity(iCarrier, iPlayer).mission()
        if mission != 0 : 
            return mission
        return self.missionIndexes()[0]

    def carrierGoal(self, iCarrier= 1, iPlayer= 1):
        mission= self.entity(iCarrier, iPlayer).mission()
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
        return [ m.tile() for m in self.entities(iPlayer) ]
    
    def encumber(self, iTile):
        return self._encumbers[iTile-1]

    # Initializing:
    def initTabletop( self, tabletop, defaultEncumberValue= 0.0):
        super(Land, self).initTabletop( tabletop )
        self.resetEncumbers( defaultEncumberValue )
        return self

    # Construction:
    def initMoves(self):
        for group in range( self.numberOfGroups() ) :
            for car in self.entities(group) :
                car.setMove(0)

    def append( self, tile, encumber= 0.0 ):
        super(Land, self).append(tile)
        self._encumbers.append(encumber)

    def setEncumber( self, iTile, value ):
        self._encumbers[iTile-1]= value
        return self

    def resetEncumbers( self, defaultValue= 0.0 ):
        self._encumbers= [ defaultValue for i in range(self.size()) ]
        return self

    def clear( self ):
        super(Land, self).clear()
        self._missions= []

    def addTile( self, aTile, encumber= 0.0 ):
        super(Land, self).appendTile(aTile)
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
            for iCarrier in range(1, self.numberOfEntities(group)+1) :
                self.entity( iCarrier, group ).setMission(0)
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
        bound= self._engine._tabletop.size()+1
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
        carrier= self.tile(iFrom).entity()
        self.tile(iFrom).clear()

        # Set on iTo
        self.tile(iTo).append(carrier)
        #carrier.setTile( iTo )
        carrier.setPose( self.tile(iTo).position(), self.orientation() )
        return iTo
    
    # Hacka.DataTree interface:
    def asDataTree( self ):
        return hacka.DataTree( self._name, [], [], [ super(Land, self).asDataTree(), self.missionsAsDataTree() ] )
    
    def missionsAsDataTree(self):
        missionDataTree= hacka.DataTree( "Missions" )
        for m in self._missions :
            missionDataTree.append( hacka.DataTree( "Mission", m.asList() ) )
        return missionDataTree
    
    def carriersAsDataTree(self):
        mobiles= hacka.DataTree( "Carriers" )
        for group in range( self.numberOfGroups() ):
            for car in self.entities( group ):
                mDataTree= hacka.DataTree( "carrier", [group, car.id(), car.mission()] )
                mobiles.append(mDataTree)
        return mobiles

    def fromDataTree( self, aDataTree ):
        self._name= aDataTree.label()
        super(Land, self).fromDataTree( aDataTree.child(1) )
        self.missionsFromDataTree(  aDataTree.child(2) )
        return self
    
    def missionsFromDataTree(self, aDataTree):
        self._missions= []
        for childDataTree in aDataTree.children() :
            self._missions.append( Mission().fromList( childDataTree.digits() ) )
        return self._missions
    
    def carriersFromDataTree(self, aDataTree):
        self.clearEntities()
        for c in aDataTree.children() :
            iPlayer= c.digit(1)
            iCarrier= c.digit(2)
            pos= c.digit(3)
            mis= c.digit(4)
            carrier= self.tileAppendEntity( pos, Entiry(iPlayer) )
            assert carrier.id() == iCarrier
            carrier.setMission(mis)
        return self._entities

    def setOnState(self, aDataTree):
        self.missionsFromDataTree( aDataTree.child(1) )
        self.carriersFromDataTree( aDataTree.child(2) )
        return aDataTree.digit(1)
    
    # Rendering :
    def renderOn(self, artist, marketBrush= tll.artist.palette.background[6]):
        self.tabletop().renderOn( artist )
        # Market:
        artist.drawPolygon(
            [6.55, 6.55, 9.5, 9.5], [2.45, -0.6, -0.6, 2.45],
            marketBrush
        )
        artist._fontSize= 20
        artist.write( 6.6, 2.2, "Market Place:", marketBrush )
        artist._fontSize= 16
        sep= 0.0
        for i in self.missionIndexes() :
            mFrom, mTo, pay, iPlayer= self.mission(i).asTuple()
            artist.write( 6.8, 1.9-sep, f".{i}", marketBrush) 
            artist.write( 7.2, 1.9-sep, f"- {mFrom} to: {mTo}", marketBrush )
            if iPlayer == 0 :
                artist.write( 8.5, 1.9-sep, f"({pay} ¢)", marketBrush )
            else :
                artist.write( 8.4, 1.9-sep, f"(Team-{iPlayer})", marketBrush )
            sep+= 0.24
        return self

