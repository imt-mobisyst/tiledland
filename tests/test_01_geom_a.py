# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry, Float2

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
    assert poss == [ Float2(1.0, 0.0),
                Float2(0.5, 0.87), Float2(0.87, 0.5), Float2(1.0, 0.0),
                Float2(0.87, -0.5), Float2(0.5, -0.87), Float2(0.0, -1.0),
                Float2(-0.5, -0.87), Float2(-0.87, -0.5), Float2(-1.0, 0.0),
                Float2(-0.87, 0.5), Float2(-0.5, 0.87), Float2(0.0, 1.0)
    ]