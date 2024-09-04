import sys
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#                T E S T  T i l e d L a n d : :  M A P                     #
# ------------------------------------------------------------------------ #
import src.tiledLand as til
from  src.tiledLand.geometry import Coord2

map= None

def test_map_generateGridMap():
    global map
    map= til.Map().setSquareGrid(
        [
            [1,1,1],
            [1,0,1],
            [1,0,0]
        ],
        til.Coord2(1.0, 1.0), 1.0
    )
    assert( map.size() == 6 )

def test_map_generateGridMap_positions():
    global map

    # Line 1
    assert( map.tile(1).center().tuple() == ( 1.5, 1.5 ) )
    # Line 2
    assert( map.tile(2).center().tuple() == ( 1.5, 2.5 ) )
    assert( map.tile(3).center().tuple() == ( 3.5, 2.5 ) )
    # Line 3
    assert( map.tile(4).center().tuple() == ( 1.5, 3.5 ) )
    assert( map.tile(5).center().tuple() == ( 2.5, 3.5 ) )
    assert( map.tile(6).center().tuple() == ( 3.5, 3.5 ) )

def test_map_generateGridMap_edges():
    global map

    # Line 1
    assert( map.adjacencies(1) == [2] )
    # Line 2
    assert( map.adjacencies(2) == [1, 4] )
    assert( map.adjacencies(3) == [6] )
    # Line 3
    assert( map.adjacencies(4) == [2, 5] )
    assert( map.adjacencies(5) == [4, 6] )
    assert( map.adjacencies(6) == [3, 5] )

def test_map_generateHexaMap():
    global map
    map= til.Map().setHexaGrid(
        [
            [1,1,1],
             [1,0,1],
            [1,0,0]
        ],
        til.Coord2(1.0, 1.0), 1.0
    )
    assert( map.size() == 6 )

def test_map_generateHexaMap_positions():
    global map

    # Line 1
    assert( map.tile(1).center().round().tuple() == ( 1.5, 1.5 ) )
    # Line 2
    assert( map.tile(2).center().round().tuple() == ( 2.0, 2.4 ) )
    assert( map.tile(3).center().round().tuple() == ( 4.0, 2.4 ) )
    # Line 3
    assert( map.tile(4).center().round().tuple() == ( 1.5, 3.2 ) )
    assert( map.tile(5).center().round().tuple() == ( 2.5, 3.2 ) )
    assert( map.tile(6).center().round().tuple() == ( 3.5, 3.2 ) )

def test_map_generateHexaMap_edges():
    global map

    # Line 1
    assert( map.adjacencies(1) == [2] )            
    # Line 2                                       # [4,5,6],
    assert( map.adjacencies(2) == [1, 4, 5] )      #  [2,0,3],
    assert( map.adjacencies(3) == [6] )         # [1,0,0]
    # Line 3
    assert( map.adjacencies(4) == [2, 5] )
    assert( map.adjacencies(5) == [2, 4, 6] )
    assert( map.adjacencies(6) == [3, 5] )