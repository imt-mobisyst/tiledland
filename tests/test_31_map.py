import sys
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#                T E S T  T i l e d L a n d : :  M A P                     #
# ------------------------------------------------------------------------ #
import src.tiledLand as til
from  src.tiledLand.geometry import Coord2

def test_map_init():
    map= til.Map()
    assert( type(map) == til.Map )
    assert( map.size() == 0 )

def test_map_addTiles():
    map= til.Map()
    assert( map.addTile( til.Tile().setFromList( [(3,1), (5,1), (5,3), (3,3)] ) ) == 1 )
    assert( map.size() == 1 )
    assert( map.addTile( til.Tile().setRegular( 9, Coord2(12.5, 3.4), 1 ) ) == 2 )
    assert( map.size() == 2 )

    count= 0
    for tile in map.tiles() :
        count+= 1
    assert( count == 2 )

def test_map_connexions():
    map= til.Map()
    map.addTile( til.Tile().setFromList( [(3,1), (5,1), (5,3), (3,3)] ) )
    map.addTile( til.Tile().setRegular( 9, Coord2(12.5, 3.4), 1 ) )
    map.addTile( til.Tile().setRegular( 3, Coord2(14.5, 2.4), 1 ) )

    assert( map.adjacencies(1) == [] )
    assert( map.adjacencies(2) == [] )
    assert( map.connexions() == [] )

    assert( map.gateIds(1) == [] )
    assert( map.gateIds(2) == [] )

    map.connect( 1, 2 )

    assert( map.adjacencies(1) == [2] )
    assert( map.adjacencies(2) == [1] )
    assert( map.adjacencies(3) == [] )

    assert( map.connexions() == [(1, 2)] )

    assert( map.gateIds(1) == [(1, 8)] )
    assert( map.gateIds(2) == [(8, 1)] )
    assert( map.gateIds(3) == [] )

    map.connect( 3, 2 )

    assert( map.adjacencies(1) == [2] )
    assert( map.adjacencies(2) == [1, 3] )
    assert( map.adjacencies(3) == [2] )

    assert( map.connexions() == [(1, 2), (2, 3)] )

    assert( map.gateIds(1) == [(1, 8)] )
    assert( map.gateIds(2) == [(8, 1), (4, 2)] )
    assert( map.gateIds(3) == [(2, 4)] )

def test_map_joins():
    map= til.Map()
    t1= til.Tile().setFromList( [(3,1), (5,1), (5,3), (3,3)] )
    t2= til.Tile().setRegular( 9, Coord2(12.5, 3.4), 1 )
    t3= til.Tile().setRegular( 3, Coord2(14.5, 2.4), 1 )

    map.addTile( t1 )
    map.addTile( t2 )
    map.addTile( t3 )

    map.connect( 1, 2 )
    map.connect( 2, 3 )

    joints= map.joints(2)

    assert( len(joints) == 2 )
    assert( joints[0].tileA() == t2 )
    assert( joints[0].tileB() == t1 )
    assert( joints[1].tileA() == t2 )
    assert( joints[1].tileB() == t3 )

    gateA, gateB= joints[0].gates()
    assert( gateA.a().round().tuple() == (12.0, 3.2) )
    assert( gateA.b().round().tuple() == (12.0, 3.6) )

    assert( gateB.a().round().tuple() == (5, 1) )
    assert( gateB.b().round().tuple() == (5, 3) )

    gateA, gateB= joints[1].gates()
    assert( gateA.a().round().tuple() == (13.0, 3.4) )
    assert( gateA.b().round().tuple() == (12.9, 3.1) )

    assert( gateB.a().round().tuple() == (14.2, 2.0) )
    assert( gateB.b().round().tuple() == (14.2, 2.8) )

