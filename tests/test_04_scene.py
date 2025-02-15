# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Body, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Scene_init():
    scene= Scene()
    assert type(scene) == Scene
    assert scene.size() == 0
    assert scene.box() == Box()

def test_Scene_initLine():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).id() == 1
    assert scene.tile(2).id() == 2
    assert scene.tile(3).id() == 3
    assert scene.tiles() == [ scene.tile(1), scene.tile(2), scene.tile(3) ]
    assert scene.edges() == []

    assert scene.tile(1).position().tuple() == (0.0, 0.0)
    assert scene.tile(1).envelope() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

    assert scene.tile(2).position().tuple() == (1.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(2).envelope() ]
    assert env == [(0.55, 0.45), (1.45, 0.45), (1.45, -0.45), (0.55, -0.45)]

    assert scene.tile(3).position().tuple() == (2.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(3).envelope() ]
    assert env == [(1.55, 0.45), (2.45, 0.45), (2.45, -0.45), (1.55, -0.45)]
    
def test_Scene_construction():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).adjacencies() == []
    assert scene.tile(2).adjacencies() == []
    assert scene.tile(3).adjacencies() == []
    scene.connect(1, 2)
    scene.connect(1, 3)
    scene.connect(2, 2)
    scene.connect(2, 1)
    scene.connect(3, 1)
    scene.connect(3, 2)
    scene.connect(3, 3)
    assert scene.tile(1).adjacencies() == [2, 3]
    assert scene.tile(2).adjacencies() == [1, 2]
    assert scene.tile(3).adjacencies() == [1, 2, 3]
    assert scene.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idScene= id(scene)
    scene.initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {scene.edges()}")
    assert( idScene == id(scene) )
    assert scene.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_Scene_str():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    scene.tile(2).append( Body(1) )

    print( f">>> {scene}." )

    assert "\n"+str(scene)+"\n" == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(1)
  - Body-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

def test_Scene_pod():
    scene= Scene().initializeLine(4)
    scene.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    scene.tile(1).position().set( 5.0, 3.0 )
    scene.tile(2).position().set( 5.0, 15.0 )
    scene.tile(3).position().set( 1.0, 9.0 )
    scene.tile(4).position().set( 9.0, 9.0 )

    print(f">>>\n{scene}")
    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(4.55, 2.55), (5.45, 3.45)⌉ adjs[2, 3, 4] bodies(0)
- Tile-2 ⌊(4.55, 14.55), (5.45, 15.45)⌉ adjs[1, 3, 4] bodies(0)
- Tile-3 ⌊(0.55, 8.55), (1.45, 9.45)⌉ adjs[1, 2] bodies(0)
- Tile-4 ⌊(8.55, 8.55), (9.45, 9.45)⌉ adjs[1, 2] bodies(0)
"""

def test_Scene_absobj():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert scene.numberOfWords() == 1
    assert scene.wordAttributes() == ["Scene"]
    assert scene.wordAttribute() == "Scene"

    assert scene.numberOfInts() == 0
    assert scene.intAttributes() == []
    
    assert scene.numberOfFloats() == 0
    assert scene.floatAttributes() == []
    
    assert scene.numberOfChildren() == 3
    assert scene.children() == [ scene.tile(1), scene.tile(2), scene.tile(3) ]

def test_Scene_copy():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert scene.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

    print("Go for the copying...")
    sceneBis= scene.copy()
    scene.connect(3, 1)

    assert type(scene) == type(sceneBis)
    assert sceneBis.size() == 3

    print(f">>>\n{sceneBis}")
    assert '\n'+ str(sceneBis) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] bodies(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] bodies(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] bodies(0)
"""

    assert sceneBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def t_est_Scene_connection():
    scene= scene.Scene(3)
    scene.connect(1, 2)
    scene.connect(2, 2)
    scene.connect(2, 3)
    scene.connect(3, 2)
    assert "\n"+str(scene) == """
Scene
- tile-1
- Edge-1 [2]
- tile-2
- Edge-2 [2, 3]
- tile-3
- Edge-3 [2]"""

    assert scene.edgesFrom(1) == [2]
    assert scene.edgesFrom(2) == [2, 3]
    assert scene.edgesFrom(3) == [2]
    
    assert scene.isEdge(1, 2)
    assert scene.isEdge(2, 2)
    assert scene.isEdge(3, 2)
    assert not scene.isEdge(2, 1)
    assert not scene.isEdge(1, 3)
    assert not scene.isEdge(3, 1)
  
def t_est_Scene_iterator():
    scene= Scene(3)
    scene.connect(1, 2)
    scene.connect(2, 2)
    scene.connect(2, 3)
    scene.connect(3, 2)

    ref= [
        [ "tile-1", [2]],
        [ "tile-2", [2, 3]],
        [ "tile-3", [2] ]
    ]
    i= 0
    for tile, edges in scene :
        assert scene.itile() == i+1
        assert str(tile) == ref[i][0]
        assert edges == ref[i][1]
        i+=1
