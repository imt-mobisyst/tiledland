# HackaGames UnitTest - `pytest`
import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland import geometry
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G E O M E T R Y
# ------------------------------------------------------------------------ #

def test_fast_load_geometry():
    aPoint= tll.Point()
    aLine= tll.Line()
    aConvex= tll.Convex()
    aGrid= tll.Grid()

def test_fast_geometry_clocks():
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

def test_fast_point_init():
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

def test_fast_point_line():
    a= Point(1.0, 1.5)
    b= Point(7.0, 3.5)

    assert not Point(5.0, 1.6).isCollidingLine(a, b)
    assert Point(5.0, 1.6).isCollidingLine(a, b, 3.0)
    assert Point(4.0, 2.5).isCollidingLine(a, b)

def test_fast_point_angle():
    # angle
    assert (round( Point(0, -1).angle( Point(0, 1) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 1).angle( Point(0, -1) ), 4 )
            == round( -math.pi, 4 ) )
    
    assert (round( Point(0, 1).angle( Point(1, 0) ), 4 )
            == round( -math.pi/2.0, 4 ) )
    
    assert (round( Point(0, 1).angle( Point(-1, 0) ), 4 )
            == round( math.pi/2.0, 4 ) )
    
    assert (round( Point(0, -12).angle( Point(0, 0.1) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 71).angle( Point(0, -51) ), 4 )
            == round( -math.pi, 4 ) )
    
    assert (round( Point(0, 2).angle( Point(14, 0) ), 4 )
            == round( -math.pi/2.0, 4 ) )
    
    assert (round( Point(0, 0.08).angle( Point(-24, 0) ), 4 )
            == round( math.pi/2.0, 4 ) )
    
    # angle (positive)
    assert (round( Point(0, -1).angleClockwise( Point(0, 1) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 1).angleClockwise( Point(0, -1) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 1).angleClockwise( Point(1, 0) ), 4 )
            == round( math.pi/2.0, 4 ) )
    
    assert (round( Point(0, 1).angleClockwise( Point(-1, 0) ), 4 )
            == round( 3*math.pi/2.0, 4 ) )
    
    assert (round( Point(0, -12).angleClockwise( Point(0, 0.1) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 71).angleClockwise( Point(0, -51) ), 4 )
            == round( math.pi, 4 ) )
    
    assert (round( Point(0, 2).angleClockwise( Point(14, 0) ), 4 )
            == round( math.pi/2.0, 4 ) )
    
    assert (round( Point(0, 0.08).angleClockwise( Point(-24, 0) ), 4 )
            == round( 3*math.pi/2.0, 4 ) )

    # random angle: 
    assert round( (Point(1.5, 1.0)-Point(3.5, 2)).angleClockwise(Point(2.5, 3.5)-Point(3.5, 2)),
            3) == 1.446

def test_fast_point_transform():
        p1= Point(1.0, -2.3)
        p2= Point(-7.5, 0.3)

        assert p1.asTuple() == (1.0, -2.3)
        assert p2.asTuple() == (-7.5, 0.3)

        p1.translate( p2 ).round(10)
        
        assert p1.asTuple() == (-6.5, -2.0)
        
        p1.negative()
        
        assert p1.asTuple() == (6.5, 2.0)
        
        p1.rotate( math.pi*0.5 ).round(10)

        print(p1)
        assert p1.asTuple() == (-2.0, 6.5)

        p1.init( 6.5, 2.0 )