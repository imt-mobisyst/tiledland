# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Body, Tile, Scene 

from src import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_pnd_scene():
    scene= Scene().initializeGrid( [[0, 1],[-1, 0]] )
    
    assert scene.testNumberOfBodies() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0
    
    bod= scene.popBodyOn(2)

    assert type(bod) == Body
    assert bod.id() == 1
    assert scene.body(1) == bod

    assert scene.testNumberOfBodies() == 1
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    bod= scene.popBodyOn(1)

    assert type(bod) == Body
    assert bod.id() == 2
    assert scene.body(2) == bod

    assert scene.testNumberOfBodies() == 2
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 1
    assert scene.tile(3).count() == 0

    bod= scene.popBodyOn(2)

    assert scene.testNumberOfBodies() == 3
    assert scene.tile(1).count() == 1
    assert scene.tile(2).count() == 2
    assert scene.tile(3).count() == 0

    print( f"---\n{scene}.")
    assert str(scene) == """Scene:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[1, 2] bodies(1)
  - Body-2 ⌊(-0.5, 0.6), (0.5, 1.6)⌉
- Tile-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 2, 3] bodies(2)
  - Body-1 ⌊(0.6, 0.6), (1.6, 1.6)⌉
  - Body-3 ⌊(0.6, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] bodies(0)"""

    scene.clearBodies()

    assert scene.testNumberOfBodies() == 0
    assert scene.tile(1).count() == 0
    assert scene.tile(2).count() == 0
    assert scene.tile(3).count() == 0