import random, hacka.py as hk

#from .artist import Artist
#from  ... import tiled

from .robot import Robot
from .world import World

class GameMaster( hk.AbsSequentialGame ) :

    # Initialization:
    def __init__( self, model, numberOfPlayers=1, numberOfRobots= 1, tic= 100, seed=False ):
        super().__init__( numberOfPlayers )
        self._seed= seed
        # GameEngine:
        assert( type(model) == World )
        self._model= model
        self._model.computeDistances()
        self._initialTic= tic
        # Initialize Players:
        iTile= 1
        for pId in range(1, numberOfPlayers+1) :
            for iRobot in range(numberOfRobots) :
                self._model.popAgentOn( iTile, pId )
                iTile+=1
        self._scores= [ 0.0 for i in range(numberOfPlayers+1) ]
    

    # Accessor :
    def score(self, iPlayer):
        return self._scores[iPlayer]
    
    def numberOfRobots(self, iPlayer=1):
        return len( self._model.agents(iPlayer) )
    
    # Game interface :
    def initialize(self):
        self._tic= self._initialTic
        self._scores= [ 0.0 for i in range( self.numberOfPlayers()+1 ) ]
        self._model.clearMissions()
        return hk.Pod( self._model.asPod( "Pick'n Del" ) ) 
    
    def moveit_initialize(self):
        if self._randomMission > 0 :
        # Clean Up.
            self._engine.clearMissions()
            for iOwner in range(self.numberOfPlayers()+1) :
                for iMob in range( 1, self._engine.numberOfMobiles(iOwner)+1 ) :
                    self._engine.mobile(iOwner, iMob).setMission(0)
        # Set missions at random:
            for i in range( self._randomMission ) :
                self.addRandomMission()
        self._engine.reInit( self._gameTic )
        return hk.Pod( self._engine.asPod("Pick'n Del") )
    
    def playerHand( self, iPlayer ):
        # Engine :
        pod= hk.Pod().fromLists( "State", "", [self._tic], self._scores )
        # Missions :
        pod.append( self.missionsAsPod() )
        # Mobiles :
        pod.append( self.mobilesAsPod() )
        return pod

    def missionsAsPod(self):
        podMissions= hk.Pod().fromLists( ["missions"] )
        i= 1
        for m in self._model.missions() :
            podMissions.append( hk.Pod().fromLists( [f"{i}"], m.list() ) )
            i+= 1
        return podMissions
    
    def missionsFromPod( self, podState ):
        self._missions= []
        for pod in podState.children() :
            self._missions.append( Mission(pod.flag(1), pod.flag(2),pod.flag(3), pod.flag(4)) )
        return self
    
    def mobilesAsPod(self):
        podMobiles= hk.Pod().fromLists( ["mobiles"] )
        for group in range( self._model.numberOfGroups() ):
            for ir in range( 1, self._model.numberOfAgents(group)+1 ):
                mobil= self._model.agent(ir, group)
                podMobiles.append( hk.Pod().fromLists( integers=[group, ir, mobil.tile(), mobil.mission() ] ) )
        return podMobiles
    
    def mobilesFromPod( self, podState ):
        self._map.clearMobiles()
        for pod in podState.children() :
            iPlayer= pod.flag(1)
            iRobot= pod.flag(2)
            pos= pod.flag(3)
            mis= pod.flag(4)
            self._map.popRobot( iPlayer, pos, mis )
        return self

    def applyPlayerAction( self, iPlayer, action ):
        # Interpret action string
        decompo= action.split(" ")
        iRobot= 1
        while len(decompo) > 0 :
            act= decompo.pop(0)
            if act == 'go' :
                clockDir= int(decompo.pop(0))
                self.setMoveAction(iPlayer, iRobot, clockDir)
            elif act == 'do' :
                missionId= int(decompo.pop(0))
                self.setMissionAction(iPlayer, iRobot, missionId)
            elif act != 'pass' :
                break
            iRobot+=1
        return True

    def setMoveAction( self, iPlayer, iRobot, clockDir ):
        # Security:
        if not(self._model.isAgent(iRobot, iPlayer) and 0 <= clockDir and clockDir <= 12):
            return False
        self._model.agent(iRobot, iPlayer).setMove(clockDir)
        return True
    
    def setMissionAction(self, iPlayer, iRobot, iMission):
        # Security:
        model= self._model
        if not( model.isAgent(iPlayer, iRobot) and model.isMission(iMission) ) :
            return False
        # Localvariable:
        robot= self.agent(iRobot, iPlayer)
        iFrom, iTo, pay, owner= self.mission(iMission).tuple()
        # Mission start:
        if robot.mission() == 0 : 
            if robot.tile() == iFrom and owner == 0 :
                robot.setMission( iMission )
                self.updateMission(iMission, iFrom, iTo, pay, iPlayer)
                return True
            return False
        # Mission end:
        if robot.mission() == iMission and robot.tile() == iTo : 
            robot.setMission(0)
            self._scores[iPlayer]+= pay
            self.updateMission(iMission, 0, iTo, 0, iPlayer)
            return True
        return False

    def applyMoveActions(self):
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
                if m[0] != m[1] and self._map.tile(m[1]).count() > 0 :
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

    def tic( self ):
        self.applyMoveActions()

    
    def isEnded( self ):
        # if the counter reach it final value
        return self.tic() == 0

    def playerScore( self, iPlayer ):
        # All players are winners.
        return self.score(iPlayer)
    
    def toward(self, iTile, iTarget):
        gameMap= self._engine.map()
        # If no need to move:
        if iTile == iTarget :
            return 0, iTile
        # Get candidates:
        clockdirs= gameMap.clockBearing(iTile)
        nextTiles= gameMap.neighbours(iTile)
        selectedDir= clockdirs[0]
        selectedNext= nextTiles[0]
        # Test all candidates:
        for clock, tile in zip( clockdirs, nextTiles ) :
            if self._distances[tile][iTarget] < self._distances[selectedNext][iTarget] :
                selectedDir= clock
                selectedNext= tile
        # Return the selected candidates:
        return selectedDir, selectedNext

    def moveOptions(self, iTile, iTarget):
        gameMap= self._engine.map()
        # If no need to move:
        if iTile == iTarget :
            return [(0, iTile)]
        # Get candidates:
        clockdirs= gameMap.clockBearing(iTile)
        nextTiles= gameMap.neighbours(iTile)
        selected= [ (clockdirs[0], nextTiles[0]) ]
        refDist= self._distances[nextTiles[0]][iTarget]
        # Test all candidates:
        for clock, tile in zip( clockdirs[1:], nextTiles[1:] ) :
            if self._distances[tile][iTarget] == refDist :
                selected.append( (clock, tile) )
            elif self._distances[tile][iTarget] < refDist :
                selected= [ (clock, tile) ]
                refDist= self._distances[tile][iTarget]
            
        # Return the selected candidates:
        return selected

    def path(self, iTile, iTarget):
        clock, tile= self.toward(iTile, iTarget)
        move= [clock]
        path= [tile]
        while tile != iTarget :
            clock, tile= self.toward(tile, iTarget)
            move.append( clock )
            path.append( tile )
        return move, path
    
    # Vips managment: 
    def initializeVipsBehavior(self):
        self._vipsGoals= [ p for p in self.vipPositions() ]

    def numberOfVips(self):
        return self._engine.numberOfMobiles(0)

    def vipPositions(self) :
        n= self.numberOfVips()
        return [ self._engine.mobilePosition(0, i) for i in range(1, n+1) ]

    def vipGoals(self) :
        return self._vipsGoals
    
    def vipMoves(self) :
        moves= []
        for p, g in zip( self.vipPositions(), self.vipGoals() ) :
            opts= self.moveOptions( p, g )
            moves.append( opts[0][0] )
        return moves
    
    def activateVips(self) :
        vipIds= range( 1, self.numberOfVips()+1 )
        for i, m in zip( vipIds, self.vipMoves() ) :
            self._engine.setMoveAction(0, i, m)
            if m == 0 :
                self._vipsGoals[i-1] = random.choice( self._vipZones )
