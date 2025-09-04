import random, hacka as hk

#from .artist import Artist
#from  ... import tiled

from .carrier import Carrier
from .world import World

class GameEngine( hk.AbsGame ) :

    # Initialization:
    def __init__( self, world, numberOfPlayers=1, numberOfCarriers= 1, tic= 10, seed=False ):
        super().__init__()
        self._seed= seed
        # GameEngine:
        assert( type(world) == World )
        self._numberOfPlayers= numberOfPlayers
        self._model= world
        self._model.clearAgents()
        self._model.computeDistances()
        self._initialTic= tic
        self._tic= 0
        # Initialize Players:
        for pId in range(1, self._numberOfPlayers+1) :
            for tileId in random.choices( range(1, self._model.size()+1 ), k = numberOfCarriers ) :
                self._model.popAgentOn( tileId, pId )
        self._scores= [ 0.0 for i in range(self._numberOfPlayers+1) ]
    
    # Game interface :
    def initialize(self):
        self._msg= [ hk.Pod("Hello player", [i]) for i in range(self._nbPlayer+1) ]
        self._tic= 0
        return hk.Pod("EchoGame", [self._nbPlayer, self._nbTics])
    
    def playerHand( self, iPlayer=1 ):
        # Engine :
        pod= hk.Pod( "State", [self._tic], self._scores )
        # Missions :
        pod.append( self._model.missionsAsPod() )
        # Mobiles :
        pod.append( self._model.carriersAsPod() )
        return pod

    def applyAction( self, action, iPlayer=1 ):
        # Interpret action string
        decompo= action.split(" ")
        iCarrier= 1
        while len(decompo) > 0 and iCarrier <= self.numberOfPlayers() :
            act= decompo.pop(0)
            if act == 'go' :
                clockDir= int(decompo.pop(0))
                self.setMoveAction(iPlayer, iCarrier, clockDir)
            elif act == 'do' :
                missionId= int(decompo.pop(0))
                self.setMissionAction(iPlayer, iCarrier, missionId)
            elif act != 'pass' :
                break
            iCarrier+=1
        return True

    def tic( self ):
        self.applyMoveActions()

    def isEnded( self ):
        # if the counter reach it final value
        return self.ticCounter() == 0

    def playerScore( self, iPlayer=1 ):
        # All players are winners.
        return self.score(iPlayer)

    def numberOfPlayers(self):
        return self._numberOfPlayers

    # Accessor :
    def world(self):
        return self._model
    
    def score(self, iPlayer):
        return self._scores[iPlayer]
    
    def numberOfCarriers(self, iPlayer=1):
        return len( self._model.agents(iPlayer) )
    
    def ticCounter(self):
        return self._tic

    # Game interface :
    def initialize(self, mission=None):
        self._tic= self._initialTic
        self._scores= [ 0.0 for i in range( self.numberOfPlayers()+1 ) ]
        self._model.clearMissions()
        if mission is None :
            self._model.addMissionAtRandom()
        else :
            self._model.addMission( mission[0], mission[1] )
        return self._model.asPod()

    def setMoveAction( self, iPlayer, iCarrier, clockDir ):
        # Security:
        if not(self._model.isAgent(iCarrier, iPlayer) and 0 <= clockDir and clockDir <= 12):
            return False
        self._model.agent(iCarrier, iPlayer).setMove(clockDir)
        return True
    
    def setMissionAction(self, iPlayer, iCarrier, iMission):
        # Security:
        model= self._model
        if not( model.isAgent(iPlayer, iCarrier) and model.isMission(iMission) ) :
            return False
        # Localvariable:
        carrier= model.agent(iCarrier, iPlayer)
        iFrom, iTo, pay, owner= model.mission(iMission).asTuple()
        # Mission start:
        if carrier.mission() == 0 : 
            if carrier.tile() == iFrom and owner == 0 :
                carrier.setMission( iMission )
                model.updateMission(iMission, iFrom, iTo, pay, iPlayer)
                return True
            return False
        # Mission end:
        if carrier.mission() == iMission and carrier.tile() == iTo : 
            carrier.setMission(0)
            self._scores[iPlayer]+= pay
            model.updateMission(iMission, 0, iTo, 0, iPlayer)
            model.addMissionAtRandom()
            return True
        return False

    def applyMoveActions(self):
        collision= 0
        # Visit all agents:
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for mobile in self._model.agents(iPlayer) :
                if mobile.move() != 0 :
                    self._model.move( mobile.tile(), mobile.move() )
                    self._scores[iPlayer]+= -1
        # Clean moves:
        self._model.initializeMoves()
        self._tic-= 1
        return collision
    
    def applyMoveActionsWithCollide(self):
        collision= 0
        reserved= []
        blocked= []
        # Get players moves:
        moves= [[]]
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            moves.append([])
            for mobile in self._model.agents(iPlayer) :
                iFrom= mobile.tile()
                iTo= self._model.clockposition( iFrom, mobile.move() )
                moves[iPlayer].append( [iFrom, iTo] )
        
        # Start Collision: 
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[0] != m[1] and self._model.tile(m[1]).count() > 0 :
                    self._scores[iPlayer]+= -100
                    collision+= 1
                    m[1]= m[0]

        # Reserve and block:
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[0] != m[1] :
                    if m[1] in reserved :
                        if m[1] not in blocked :
                            blocked.append(m[1])
                    else:
                        reserved.append(m[1])

        # Apply non-bloked moves :
        for iPlayer in range( 1, self._numberOfPlayers+1 ):
            for m in moves[iPlayer] :
                if m[1] in blocked :
                    self._scores[iPlayer]+= -100
                    collision+= 1
                else:
                    self._model.teleport( m[0], m[1] )
        
        # Clean moves:
        self._model.initializeMoves()
        self._tic-= 1
        return collision

    
    
    def toward(self, iTile, iTarget):
        world= self.world()
        # If no need to move:
        if iTile == iTarget :
            return 0, iTile
        # Get candidates:
        clockdirs= world.clockBearing(iTile)
        nextTiles= world.adjacencies(iTile)
        selectedDir= clockdirs[0]
        selectedNext= nextTiles[0]
        # Test all candidates:
        for clock, tile in zip( clockdirs, nextTiles ) :
            if world._distances[tile][iTarget] < world._distances[selectedNext][iTarget] :
                selectedDir= clock
                selectedNext= tile
        # Return the selected candidates:
        return selectedDir, selectedNext

    def path(self, iTile, iTarget):
        clock, tile= self.toward(iTile, iTarget)
        move= [clock]
        path= [tile]
        while tile != iTarget :
            clock, tile= self.toward(tile, iTarget)
            move.append( clock )
            path.append( tile )
        return move, path
    
class GameMaster( hk.SequentialGameMaster ) :
    def __init__( self, world, numberOfPlayers=1, numberOfCarriers= 1, tic= 10, seed=False ):
        super().__init__(
            GameEngine( world, numberOfPlayers, numberOfCarriers, tic, seed ), 
            numberOfPlayers
    )
