# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry
from src.tiledland.geometry import Point, Line

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

def test_point_init():
    p1= Point()
    assert type(p1) == Point
    assert p1.asTuple() == (0.0, 0.0)

    assert p1.norm2() == 0.0

    p2= Point(1.0, 1.0)
    assert p2.asTuple() == (1.0, 1.0)
    assert p2.norm2() == 2.0

    p3= Point(2.0, 0.0)
    assert p3.asTuple() == (2.0, 0.0)
    assert p3.norm2() == 4.0
    
    assert not p1.isColliding(p2)
    assert not p1.isColliding(p3)
    assert p1.isColliding(p2, 3.0)

def test_point_line():
    a= Point(1.0, 1.5)
    b= Point(7.0, 3.5)

    assert not Point(5.0, 1.6).isCollidingLine(a, b)
    assert Point(5.0, 1.6).isCollidingLine(a, b, 3.0)
    assert Point(4.0, 2.5).isCollidingLine(a, b)
