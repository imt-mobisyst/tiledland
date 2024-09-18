import sys
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#                T E S T  T i l e d L a n d : :  M A P                     #
# ------------------------------------------------------------------------ #
from src.tiledLand import Map, Tile
from src.tiledLand.geometry import Coord2

def test_map_initGraph():
    map= Map(
        [ Coord2(12.5, 3.4), Coord2(14.5, 2.4), Coord2(10.5, 0.8) ],
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1.0 )
    )
    assert( map.size() == 3 )

    assert( map.tile(1).id()  == 1 )
    assert( map.tile(2).id()  == 2 )
    assert( map.tile(3).id()  == 3 )
    
    assert( map.adjacencies(1) == [] )
    assert( map.adjacencies(2) == [] )
    assert( map.adjacencies(3) == [] )
    assert( map.connexions() == [] )

    map= Map(
        [Coord2(1, 3), Coord2(3, 3), Coord2(3, 1), Coord2(1, 1)],
        [ (1,2), (2,3), (2,4), (4,1) ],
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1 )
    )
    assert( map.size() == 4 )

    assert( map.adjacencies(1) == [2, 4] )
    assert( map.adjacencies(2) == [1, 3, 4] )
    assert( map.adjacencies(3) == [2] )
    assert( map.adjacencies(4) == [2, 1] )
    assert( map.connexions() == [(1, 2), (1, 4), (2, 3), (2, 4)] )

nodes= [
    Coord2(-4.0, 1.0), Coord2(-4.0, 4.0), Coord2(-3.6, 7.0),
    Coord2(-1.4, 3.0), Coord2(-1.0, 0.8), Coord2(-0.8, 5.4)
]
nodes= [
    (n.scale(1.3)+Coord2(8, -0.2)).round(2)
    for n in nodes
]
    
edges= [ (1,2), (2,3), (2,4), (3,6), (4,1), (4,5), (4,6) ]

def test_map_edgesToPath():
    map= Map(
        nodes, edges,
        tileModel= Tile().setRegular( 12, Coord2(0.0, 0.0), 1 )
    )

    assert( map.size() == 6 )
    assert( len( map.connexions() ) == 7 )

    map.setEdgeAsPath()

    assert( map.size() == 13 )
    assert( len( map.connexions() ) == 14 )
