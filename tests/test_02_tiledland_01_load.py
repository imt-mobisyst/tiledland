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
    agent= tll.Agent()
    tile= tll.Tile()
    scene= tll.Scene()

def test_load_local_tllihm():
    support= tll.Support()
    support2= tll.SupportSVG()
    support3= tll.SupportPNG()
    artist= tll.Artist()

import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_load_geometry():
    point= tll.Point()
    line= tll.Line()
    convex= tll.Convex()
    grid= tll.Grid()

def test_load_tllcore():
    agent= tll.Agent()
    tile= tll.Tile()
    scene= tll.Scene()

def test_load_local_tllihm():
    support= tll.Support()
    support2= tll.SupportSVG()
    support3= tll.SupportPNG()
    artist= tll.Artist()
