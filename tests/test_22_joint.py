import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T  T i l e d M a p : :  T I L E                  #
# ------------------------------------------------------------------------ #
import src.tiledMap as tim

def test_Joint_init():
    joint= tim.Joint()
    assert( type(joint) == tim.Joint )
