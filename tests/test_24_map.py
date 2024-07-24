import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#                T E S T  T i l e d M a p : :  M A P                       #
# ------------------------------------------------------------------------ #
import src.tiledMap as tim

def test_map_init():
    map= tim.Map()
    assert( type(map) == tim.Map )
    assert( map.size() == 0 )
