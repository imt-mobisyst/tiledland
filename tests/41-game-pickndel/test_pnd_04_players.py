import sys, hacka.py as hk

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_basicBot_wakeUp():
    world= pnd.World().initializeGrid([[0, 0], [0, 0]])
    master= pnd.GameMaster( world )
    bot= pnd.BasicBot()

    initPod= master.initialize( (1, 2) )

    print( f">>> {initPod}.")
    assert str(initPod) == """Pick'nDel:
- Scene:
  - Tile: [1, 0, 1, 2, 3] [0.0, 1.1]
    - Shape: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
    - Agent: [1, 1, 11, 1] [0.0, 1.1]
      - Shape: [-0.18477590650225736, 0.07653668647301798, -0.07653668647301795, 0.18477590650225736, 0.07653668647301798, 0.18477590650225736, 0.18477590650225736, 0.07653668647301796, 0.18477590650225736, -0.07653668647301796, 0.07653668647301798, -0.18477590650225736, -0.07653668647301795, -0.18477590650225736, -0.18477590650225736, -0.07653668647301798]
  - Tile: [2, 0, 1, 2, 4] [1.1, 1.1]
    - Shape: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
  - Tile: [3, 0, 1, 3, 4] [0.0, 0.0]
    - Shape: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
  - Tile: [4, 0, 2, 3, 4] [1.1, 0.0]
    - Shape: [-0.5, 0.5, 0.5, 0.5, 0.5, -0.5, -0.5, -0.5]
- Missions:
  - Mission: [1, 2, 10, 0]"""

    bot.wakeUp( 1, 1, initPod )

    initBotPod= hk.Pod( bot._model.asPod( "Pick'nDel" ) )

    assert str(initBotPod) == str(initPod)

    bot._model.render()

    assert bot.playerId() == 1
    assert bot.model().numberOfAgents( bot.playerId() ) == 1

    statePod= master.playerHand(1)
    print( f">>> {statePod}.")
    assert str(statePod) == """State: [10] [0.0, 0.0]
- Missions:
  - Mission: [1, 2, 10, 0]
- Carriers:
  - carrier: [1, 1, 1, 0]"""

    bot.perceive(statePod)
    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

    assert str(bot.model().asPod()) == str(master.world().asPod())

    master.world().addMission(2, 4, 12)
    
    statePod= master.playerHand(1)
    print( f">>> {statePod}.")
    assert str(statePod) == """State: [10] [0.0, 0.0]
- Missions:
  - Mission: [1, 2, 10, 0]
  - Mission: [2, 4, 12, 0]
- Carriers:
  - carrier: [1, 1, 1, 0]"""

    bot.perceive(statePod)

    bot.model().render()

    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

def test_basicBot_loop():
    world= pnd.World().initializeGrid([[0, 0], [0, 0]])
    master= pnd.GameMaster( world, tic= 10 )

    bot= pnd.BasicBot()

    assert master.world().missionIndexes() == []
    assert master.initialize((1, 2))
    assert master.world().missionIndexes() == [1]

    t= 10
    while t > 0 :
        assert not master.isEnded()
        assert master.ticCounter() == t
        master.tic()
        t-= 1
    
    assert( master.isEnded() )
