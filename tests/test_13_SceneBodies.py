# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Shape, Box
from src.tiledland import Agent, Tile, Scene 

from src import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_pnd_scene():
    scene= Scene().initializeGrid( [[0, 1],[-1, 0]] )
    
    assert scene.testNumberOfAgents() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0
    
    bod= scene.popAgentOn(2)

    assert type(bod) == Agent
    assert bod.id() == 1
    assert scene.agent(1) == bod

    assert scene.testNumberOfAgents() == 1
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    bod= scene.popAgentOn(1)

    assert type(bod) == Agent
    assert bod.id() == 2
    assert scene.agent(2) == bod

    assert scene.testNumberOfAgents() == 2
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    bod= scene.popAgentOn(2)

    assert scene.testNumberOfAgents() == 3
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 2
    assert scene.tile(3).count() == 0

    print( f"---\n{scene}.")
    assert str(scene) == """Scene:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[1, 2] agents(1)
  - Agent-2 ⌊(-0.2, 0.9), (0.2, 1.3)⌉
- Tile-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 2, 3] agents(2)
  - Agent-1 ⌊(0.9, 0.9), (1.3, 1.3)⌉
  - Agent-3 ⌊(0.9, 0.9), (1.3, 1.3)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] agents(0)"""

    scene.clearAgents()

    assert scene.testNumberOfAgents() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0