import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#                T E S T  T i l e d M a p : :  M A P                       #
# ------------------------------------------------------------------------ #
import src.tiledLand as tim

def test_map_init():
    map= tim.Map()
    assert( type(map) == tim.Map )
    assert( map.size() == 0 )

def test_map_addTiles():
    map= tim.Map()
    assert( map.addTile( tim.Tile([(3,1), (5,1), (5,3), (3,3)]) ) == 0 )
    assert( map.size() == 1 )
    assert( map.addNewTile( (12.5, 3.4) ) == 1 )
    assert( map.size() == 2 )

    count= 0
    for tile in map.tiles() :
        count+= 1
    assert( count == 2 )
        