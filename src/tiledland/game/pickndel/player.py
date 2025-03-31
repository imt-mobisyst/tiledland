import time
from hacka import AbsPlayer
from .world import World

class BasicBot( AbsPlayer ):

    # Constructor:
    def __init__(self):
        super().__init__()
        self._model= World()
        self._id= 0
        self._sumResult= 0.0
        self._countResult= 0
        self._tic= 0

    # Accessor:
    def model(self):
        return self._model
    
    def ticCounter(self):
        return self._tic

    def playerId(self):
        return self._id
    
    def averageResult(self):
        return (self._sumResult/self._countResult)

    # Construction
    def resetResult(self):
        self._sumResult= 0.0
        self._countResult= 0
        return self

    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        # Initialize from gamePod:
        self._model.fromPod(gamePod)
        self._id= playerId

    def perceive(self, podState):
        # update the game state:
        self._tic= self._model.setOnPodState(podState)

    def decide(self):
        return "pass"
    
    def sleep(self, result):
        self._sumResult+= result
        self._countResult+= 1
    
class ShellPlayer( BasicBot ):
    def __init__(self):
        super().__init__()
        self._action= "pass"
    
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        super().wakeUp(playerId, numberOfPlayers, gamePod)
        self._action= "pass"
        self.model().render()
        print( f"Output image : ./shot-pickndel.png" )
        print( "New game..." )
        print( "Possible Actions:" )
        print( "   - do missionId" )
        print( "   - go clockDirection" )
        print( "   - pass" )
        print( "   - stop (will 'pass' until the game ends)" )

    def perceive(self, podState):
        super().perceive(podState)
        self.model().render()

    def decide(self):
        if self._action != "stop" :
            msg= f'tic-{ self.ticCounter() }'
            msg+= f', tile-{ self._model.carrierTile() }'
            msg+= f', goal-{ self._model.carrierGoal() }'
            msg+= '\n> Enter your action: '
            self._action = input(msg)
        if self._action == "stop" :
            return "pass"
        return self._action

    def sleep(self, result):
        super().sleep(result)
        print( f"End on result: {result}" )

