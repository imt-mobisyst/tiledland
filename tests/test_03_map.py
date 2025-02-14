# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from hacka.py.pod import Pod
from src.tiledland import Tile, Map 

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Map_init():
    tile= Tile(42)
    assert tile.number() == 42
    
    map= Map().initializeLine(3)
    assert map.tile(1).number() == 1
    assert map.tile(2).number() == 2
    assert map.tile(3).number() == 3
    assert map.tiles() == [ map.tile(1), map.tile(2), map.tile(3) ]
    assert map.edges() == []

    assert map.tile(1).center().tuple() == (0.0, 0.0)
    assert map.tile(1).envelope() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

    assert map.tile(2).center().tuple() == (1.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in map.tile(2).envelope() ]
    assert env == [(0.55, 0.45), (1.45, 0.45), (1.45, -0.45), (0.55, -0.45)]

    assert map.tile(3).center().tuple() == (2.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in map.tile(3).envelope() ]
    assert env == [(1.55, 0.45), (2.45, 0.45), (2.45, -0.45), (1.55, -0.45)]
    
    assert map.shapes() == [map.shape()]
    env= [ (round(x, 2), round(y, 2)) for x, y in map.shape().envelope() ]
    assert env == [(-0.25, 0.1), (-0.1, 0.25), (0.1, 0.25), (0.25, 0.1), (0.25, -0.1), (0.1, -0.25), (-0.1, -0.25), (-0.25, -0.1)]

def test_Map_construction():
    map= Map().initializeLine(3)
    assert map.tile(1).adjacencies() == []
    assert map.tile(2).adjacencies() == []
    assert map.tile(3).adjacencies() == []
    map.connect(1, 2)
    map.connect(1, 3)
    map.connect(2, 2)
    map.connect(2, 1)
    map.connect(3, 1)
    map.connect(3, 2)
    map.connect(3, 3)
    assert map.tile(1).adjacencies() == [2, 3]
    assert map.tile(2).adjacencies() == [1, 2]
    assert map.tile(3).adjacencies() == [1, 2, 3]
    assert map.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idMap= id(map)
    map.initializeLine(3)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {map.edges()}")
    assert( idMap == id(map) )
    assert map.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]


def test_Map_str():
    map= Map().initializeLine(3)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    map.tile(2).append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    print( f">>> {map}." )

    assert "\n"+str(map)+"\n" == """
Map:
- Shape-0/8 [(-0.25, -0.25), (0.25, 0.25)]
- Tile-1/0 center: (0.0, 0.0) adjs: [1, 3] pieces(0)
- Tile-2/0 center: (1.0, 0.0) adjs: [1, 2] pieces(1)
  - Piece: dragon [10, 3] [22.0]
- Tile-3/0 center: (2.0, 0.0) adjs: [2] pieces(0)
"""

def test_Map_pod():
    map= Map().initializeLine(4)
    map.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    map.tile(1).setCenter( 5.0, 3.0 )
    map.tile(2).setCenter( 5.0, 15.0 )
    map.tile(3).setCenter( 1.0, 9.0 )
    map.tile(4).setCenter( 9.0, 9.0 )

    map.shape().round(2)
    
    mapPod= map.asPod()
    print(f">>>1 {mapPod}")
    assert '\n'+ str(mapPod) +'\n' == """
Map:
- Shape: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    mapPod= Map().fromPod( map.asPod() ).asPod()
    print(f">>>2 {mapPod}")
    assert '\n'+ str(mapPod) +'\n' == """
Map:
- Shape: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    print(f">>> {mapPod.dump()}")
    assert '\n'+ mapPod.dump() +'\n' == """
Map - 0 0 0 5 :
Shape - 0 1 16 0 : 0 -0.25 0.1 -0.1 0.25 0.1 0.25 0.25 0.1 0.25 -0.1 0.1 -0.25 -0.1 -0.25 -0.25 -0.1
Tile - 0 5 10 0 : 1 0 2 3 4 5.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 2 0 1 3 4 5.0 15.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 3 0 1 2 1.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 4 0 1 2 9.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
"""


def test_Map_copy():
    map= Map().initializeLine(3)

    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    mapBis= map.copy()

    map.connect(3, 1)

    assert type(map) == type(mapBis)
    assert mapBis.size() == 3
    assert mapBis.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def t_est_Map_connection():
    map= map.Map(3)
    map.connect(1, 2)
    map.connect(2, 2)
    map.connect(2, 3)
    map.connect(3, 2)
    assert "\n"+str(map) == """
Map
- tile-1
- Edge-1 [2]
- tile-2
- Edge-2 [2, 3]
- tile-3
- Edge-3 [2]"""

    assert map.edgesFrom(1) == [2]
    assert map.edgesFrom(2) == [2, 3]
    assert map.edgesFrom(3) == [2]
    
    assert map.isEdge(1, 2)
    assert map.isEdge(2, 2)
    assert map.isEdge(3, 2)
    assert not map.isEdge(2, 1)
    assert not map.isEdge(1, 3)
    assert not map.isEdge(3, 1)
  
def t_est_Map_iterator():
    map= Map(3)
    map.connect(1, 2)
    map.connect(2, 2)
    map.connect(2, 3)
    map.connect(3, 2)

    ref= [
        [ "tile-1", [2]],
        [ "tile-2", [2, 3]],
        [ "tile-3", [2] ]
    ]
    i= 0
    for tile, edges in map :
        assert map.itile() == i+1
        assert str(tile) == ref[i][0]
        assert edges == ref[i][1]
        i+=1
