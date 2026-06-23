import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_load_local_geometry():
    point= tll.Point()
    line= tll.Line()
    convex= tll.Convex()
    grid= tll.Grid()
    # plane= localTll.Plane()

def test_load_local_tllcore():
    entity= tll.Entity()
    agent= tll.Agent()
    tile= tll.Tile()
    map= tll.Map()

def test_load_local_tllihm():
    artist= tll.Artist()

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - E N T I T Y
# ------------------------------------------------------------------------ #

