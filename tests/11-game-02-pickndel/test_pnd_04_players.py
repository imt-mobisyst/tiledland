import sys, hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_basicBot_wakeUp():
    world= pnd.World("BasicWorld").initGrid([[0, 0], [0, 0]])
    game= pnd.GameEngine( world )
    world.teleport( world.agent(1, 1).tile(), 4 )

    bot= pnd.BasicBot()

    initDT= game.init( (1, 2) )
    initDT.round(3)

    print( f"---\n{initDT}.")
    assert str(initDT) == """BasicWorld : :
- Map : : 0.01
  - Tile : 1 0 2 3 : 0.0 1.1
    - Convex : : -0.5 -0.5 -0.5 0.5 0.5 0.5 0.5 -0.5
  - Tile : 2 0 1 4 : 1.1 1.1
    - Convex : : -0.5 -0.5 -0.5 0.5 0.5 0.5 0.5 -0.5
  - Tile : 3 0 1 4 : 0.0 0.0
    - Convex : : -0.5 -0.5 -0.5 0.5 0.5 0.5 0.5 -0.5
  - Tile : 4 0 2 3 : 1.1 0.0
    - Convex : : -0.5 -0.5 -0.5 0.5 0.5 0.5 0.5 -0.5
    - Agent : 1 1 11 4 : 1.1 0.0
      - Convex : : -0.185 -0.077 -0.185 0.077 -0.077 0.185 0.077 0.185 0.185 0.077 0.185 -0.077 0.077 -0.185 -0.077 -0.185
- Missions : :
  - Mission : 1 2 124 0 :"""

    bot.wakeUp( 1, 1, initDT )

    initBotDT= bot._model.asDataTree()

    assert str(initBotDT) == str(initBotDT)

    bot._model.render()

    assert bot.playerId() == 1
    assert bot.model().numberOfAgents( bot.playerId() ) == 1

    stateDT= game.playerHand(1)
    print( f">>> {stateDT}.")
    assert str(stateDT) == """State : 10 : 0.0 0.0
- Missions : :
  - Mission : 1 2 124 0 :
- Carriers : :
  - carrier : 1 1 4 0 :"""

    bot.perceive(stateDT)
    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

    assert str(bot.model().asDataTree()) == str(game.world().asDataTree())

    game.world().addMission(2, 4, 112)
    
    stateDT= game.playerHand(1)
    print( f">>> {stateDT}.")
    assert str(stateDT) == """State : 10 : 0.0 0.0
- Missions : :
  - Mission : 1 2 124 0 :
  - Mission : 2 4 112 0 :
- Carriers : :
  - carrier : 1 1 4 0 :"""

    bot.perceive(stateDT)

    bot.model().render()

    assert bot.ticCounter() == 10
    assert bot.decide() == "pass"

def test_basicBot_loop():
    world= pnd.World().initGrid([[0, 0], [0, 0]])
    game= pnd.GameEngine( world, tic= 10 )

    bot= pnd.BasicBot()

    assert game.world().missionIndexes() == []
    assert game.init((1, 2))
    assert game.world().missionIndexes() == [1]

    t= 10
    while t > 0 :
        assert not game.isEnded()
        assert game.ticCounter() == t
        game.tic()
        t-= 1
    
    assert( game.isEnded() )
