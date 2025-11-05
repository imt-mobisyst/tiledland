# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry as geo

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_geometry_clocks():
    assert (
        [ round(x, 2) for x in geo.clockAngles ]
        == [0.0, 1.05, 0.52, 0.0, -0.52, -1.05, -1.57, -2.09, -2.62, 3.14, 2.62, 2.09, 1.57]
    )

    print( type(geo.clockPositions[0]) )
    poss= [ geo.point_round(p, 2) for p in geo.clockPositions ]
    print( ', '.join( [ str(p) for p in poss ]  ) )
    assert poss == [ geo.Point(1.0, 0.0),
                geo.Point(0.5, 0.87), geo.Point(0.87, 0.5), geo.Point(1.0, 0.0),
                geo.Point(0.87, -0.5), geo.Point(0.5, -0.87), geo.Point(0.0, -1.0),
                geo.Point(-0.5, -0.87), geo.Point(-0.87, -0.5), geo.Point(-1.0, 0.0),
                geo.Point(-0.87, 0.5), geo.Point(-0.5, 0.87), geo.Point(0.0, 1.0)
    ]