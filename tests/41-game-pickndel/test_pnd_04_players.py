import sys, hacka as hk

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_basicBot_wakeUp():
    world= pnd.World("BasicWorld").initializeGrid([[0, 0], [0, 0]])
    game= pnd.GameEngine( world )
    world.teleport( world.agent(1, 1).tile(), 4 )

    bot= pnd.BasicBot()

    initPod= game.initialize( (1, 2) )

    print( f">>> {initPod}.")
    assert str(initPod) == """BasicWorld : :
- Scene:
  - Tile: [1, 0, 1, 2, 3] [0.0, 1.1]
    - Convex: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
  - Tile: [2, 0, 1, 2, 4] [1.1, 1.1]
    - Convex: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
  - Tile: [3, 0, 1, 3, 4] [0.0, 0.0]
    - Convex: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
  - Tile: [4, 0, 2, 3, 4] [1.1, 0.0]
    - Convex: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
    - Agent: [1, 1, 11, 4] [1.1, 0.0]
      - Convex: [-0.18477590650225736, 0.07653668647301798, -0.07653668647301795, 0.18477590650225736, 0.07653668647301798, 0.18477590650225736, 0.18477590650225736, 0.07653668647301796, 0.18477590650225736, -0.07653668647301796, 0.07653668647301798, -0.18477590650225736, -0.07653668647301795, -0.18477590650225736, -0.18477590650225736, -0.07653668647301798]
- Missions : :
  - Mission : 1 2 124 0 :"""

    bot.wakeUp( 1, 1, initPod )

    initBotPod= bot._model.asPod()

    assert str(initBotPod) == str(initPod)

    bot._model.render()

    assert bot.playerId() == 1
    assert bot.model().numberOfAgents( bot.playerId() ) == 1

    statePod= game.playerHand(1)
    print( f">>> {statePod}.")
    assert str(statePod) == """State : 10 : 0.0 0.0
- Missions : :
  - Mission : 1 2 124 0 :
- Carriers : :
  - carrier : 1 1 4 0 :"""

    bot.perceive(statePod)
    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

    assert str(bot.model().asPod()) == str(game.world().asPod())

    game.world().addMission(2, 4, 112)
    
    statePod= game.playerHand(1)
    print( f">>> {statePod}.")
    assert str(statePod) == """State : 10 : 0.0 0.0
- Missions : :
  - Mission : 1 2 124 0 :
  - Mission : 2 4 112 0 :
- Carriers : :
  - carrier : 1 1 4 0 :"""

    bot.perceive(statePod)

    bot.model().render()

    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

def test_basicBot_loop():
    world= pnd.World().initializeGrid([[0, 0], [0, 0]])
    game= pnd.GameEngine( world, tic= 10 )

    bot= pnd.BasicBot()

    assert game.world().missionIndexes() == []
    assert game.initialize((1, 2))
    assert game.world().missionIndexes() == [1]

    t= 10
    while t > 0 :
        assert not game.isEnded()
        assert game.ticCounter() == t
        game.tic()
        t-= 1
    
    assert( game.isEnded() )
