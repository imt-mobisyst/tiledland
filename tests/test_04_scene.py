# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Scene_init():
    tile= Tile(42)
    assert tile.number() == 42
    
    scene= Scene().initializeLine(3)
    assert scene.tile(1).number() == 1
    assert scene.tile(2).number() == 2
    assert scene.tile(3).number() == 3
    assert scene.tiles() == [ scene.tile(1), scene.tile(2), scene.tile(3) ]
    assert scene.edges() == []

    assert scene.tile(1).center().tuple() == (0.0, 0.0)
    assert scene.tile(1).envelope() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

    assert scene.tile(2).center().tuple() == (1.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(2).envelope() ]
    assert env == [(0.55, 0.45), (1.45, 0.45), (1.45, -0.45), (0.55, -0.45)]

    assert scene.tile(3).center().tuple() == (2.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(3).envelope() ]
    assert env == [(1.55, 0.45), (2.45, 0.45), (2.45, -0.45), (1.55, -0.45)]
    
    assert scene.shapes() == [scene.shape()]
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.shape().envelope() ]
    assert env == [(-0.25, 0.1), (-0.1, 0.25), (0.1, 0.25), (0.25, 0.1), (0.25, -0.1), (0.1, -0.25), (-0.1, -0.25), (-0.25, -0.1)]

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
    #scene.tile(2).append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    print( f">>> {scene}." )

    assert "\n"+str(scene)+"\n" == """
Scene:
- Shape-0/8 [(-0.25, -0.25), (0.25, 0.25)]
- Tile-1/0 center: (0.0, 0.0) adjs: [1, 3] pieces(0)
- Tile-2/0 center: (1.0, 0.0) adjs: [1, 2] pieces(1)
  - Piece: dragon [10, 3] [22.0]
- Tile-3/0 center: (2.0, 0.0) adjs: [2] pieces(0)
"""

def test_Scene_pod():
    scene= Scene().initializeLine(4)
    scene.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    scene.tile(1).setCenter( 5.0, 3.0 )
    scene.tile(2).setCenter( 5.0, 15.0 )
    scene.tile(3).setCenter( 1.0, 9.0 )
    scene.tile(4).setCenter( 9.0, 9.0 )

    scene.shape().round(2)
    
    scenePod= scene.asPod()
    print(f">>>1 {scenePod}")
    assert '\n'+ str(scenePod) +'\n' == """
Scene:
- Shape: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    scenePod= Scene().fromPod( scene.asPod() ).asPod()
    print(f">>>2 {scenePod}")
    assert '\n'+ str(scenePod) +'\n' == """
Scene:
- Shape: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    print(f">>> {scenePod.dump()}")
    assert '\n'+ scenePod.dump() +'\n' == """
Scene - 0 0 0 5 :
Shape - 0 1 16 0 : 0 -0.25 0.1 -0.1 0.25 0.1 0.25 0.25 0.1 0.25 -0.1 0.1 -0.25 -0.1 -0.25 -0.25 -0.1
Tile - 0 5 10 0 : 1 0 2 3 4 5.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 2 0 1 3 4 5.0 15.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 3 0 1 2 1.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 4 0 1 2 9.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
"""


def test_Scene_copy():
    scene= Scene().initializeLine(3)

    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    sceneBis= scene.copy()

    scene.connect(3, 1)

    assert type(scene) == type(sceneBis)
    assert sceneBis.size() == 3
    assert sceneBis.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

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
