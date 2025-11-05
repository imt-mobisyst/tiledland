# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry as geo
from src.tiledland import tile

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_geometry_clocks():
    assert (
        [ round(x, 2) for x in tile.clockAngles ]
        == [0.0, 1.05, 0.52, 0.0, -0.52, -1.05, -1.57, -2.09, -2.62, 3.14, 2.62, 2.09, 1.57]
    )

    print( type(tile.clockPositions[0]) )
    poss= [ geo.pointRounded(p, 2) for p in tile.clockPositions ]
    print( ', '.join( [ str(p) for p in poss ]  ) )
    assert poss == [ geo.Point(1.0, 0.0),
                geo.Point(0.5, 0.87), geo.Point(0.87, 0.5), geo.Point(1.0, 0.0),
                geo.Point(0.87, -0.5), geo.Point(0.5, -0.87), geo.Point(0.0, -1.0),
                geo.Point(-0.5, -0.87), geo.Point(-0.87, -0.5), geo.Point(-1.0, 0.0),
                geo.Point(-0.87, 0.5), geo.Point(-0.5, 0.87), geo.Point(0.0, 1.0)
    ]