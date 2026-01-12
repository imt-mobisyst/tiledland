# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G E O M E T R Y
# ------------------------------------------------------------------------ #

def test_geometry_clocks():
    assert (
        [ round(x, 2) for x in geometry.clockAngles ]
        == [0.0, 1.05, 0.52, 0.0, -0.52, -1.05, -1.57, -2.09, -2.62, 3.14, 2.62, 2.09, 1.57]
    )
    poss= [ p.round(2) for p in geometry.clockPositions ]
    print( ', '.join( [ p.str() for p in poss ]  ) )
    assert poss == [ Point(1.0, 0.0),
                Point(0.5, 0.87), Point(0.87, 0.5), Point(1.0, 0.0),
                Point(0.87, -0.5), Point(0.5, -0.87), Point(0.0, -1.0),
                Point(-0.5, -0.87), Point(-0.87, -0.5), Point(-1.0, 0.0),
                Point(-0.87, 0.5), Point(-0.5, 0.87), Point(0.0, 1.0)
    ]
