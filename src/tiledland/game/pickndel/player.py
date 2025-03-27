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

    # Accessor:
    def model(self):
        return self._model
    
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
        self._model.setOnPodState(podState)

    def decide(self):
        return "pass"
    
    def sleep(self, result):
        self._sumResult+= result
        self._countResult+= 1

class BlindBot( BasicBot ):
    def __init__(self, actionsList= ['pass'], numberRobots=1):
        super().__init__()
        self._actions= actionsList
        self._step= -1
        self._fleetSize= numberRobots

    def decide(self):
        # Follow the order
        self._step+= 1
        if self._step == len(self._actions) :
            self._step= 0
        return self._actions[self._step]
    
class ShellPlayer( BasicBot ):
    def __init__(self):
        super().__init__()
        self._action= "go"
    
    # Player interface :
    def wakeUp(self, playerId, numberOfPlayers, gamePod):
        super().wakeUp(playerId, numberOfPlayers, gamePod)
        self.model().render()
        print( f"Output image : ./shot-moveIt.png" )
        self._action= "go"
        print( "New game..." )
        print( "Possible Actions:" )
        print( "   - [mission robotId missionId ...] move robotId clockDirection ... or pass" )
        print( "   - pass" )
        print( "   - stop (will 'pass' until the game ends)" )
        print( "the mission part is optional and only one action per robot will be achieved" )

    def perceive(self, statePod):
        super().perceive(statePod)
        self.model().render()

    def decide(self):
        if self._action != "stop" :
            msg= f'tic-{ self.model().tic() } | score { self.model().score(self._id) }'
            msg+= ' - Enter your action: '
            self._action = input(msg)
        if self._action == "stop" :
            return "pass"
        return self._action

    def sleep(self, result):
        super().sleep(result)
        print( f"End on result: {result}" )
