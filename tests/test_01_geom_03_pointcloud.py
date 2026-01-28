# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import geometry
from src.tiledland.geometry import Point, Line

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G E O M E T R Y
# ------------------------------------------------------------------------ #

def test_geometry_sortRadial():
    points= [
        Point(1.5, 1),
        Point(6, 3),
        Point(5, 1.5),
        Point(2.5, 3.5)
    ]
    center= Point(3.5, 2)

    points= center.sortRadial(points)

    print( [ p.asTuple() for p in points ] )
    assert ( [ p.asTuple() for p in points ]
            == [ (1.5, 1.0), (2.5, 3.5), (6.0, 3.0), (5, 1.5)] )
    
    # second test:
    points= [
        Point(-0.3, 0.17), Point(-0.0, 0.35), Point(0.3, 0.18),
        Point(0.3, -0.17), Point(0.0, -0.35), Point(-0.3, -0.18)
    ]
    center= Point(0.0, 0.0)

    points= center.sortRadial(points)

    print( [ p.asTuple() for p in points ] )
    assert ( [ p.asTuple() for p in points ]
            == [(-0.3, -0.18), (-0.3, 0.17), (-0.0, 0.35),
                (0.3, 0.18), (0.3, -0.17), (0.0, -0.35)] )
    
    # third test:
    points= [
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5),
        Point(4.5, 2.5),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ]
    center= Point(5.0, 2.75)

    points= center.sortRadial(points)

    print( [ p.asTuple() for p in points ] )
    assert ( [ p.asTuple() for p in points ]
            == [(1.0, 1.0), (5.5, 5.0), (9.0, 4.5),
                (8.5, 1.5), (6.0, 0.5), (4.5, 2.5)] )
    
    points= [
        Point(4.5, 2.5), Point(9.0, 4.5), Point(8.5, 1.5),
        Point(1.0, 1.0), Point(5.5, 5.0), Point(6.0, 0.5)
    ]
    points= center.sortRadial(points)

    print( [ p.asTuple() for p in points ] )
    assert ( [ p.asTuple() for p in points ]
            == [(1.0, 1.0), (5.5, 5.0), (9.0, 4.5),
                (8.5, 1.5), (6.0, 0.5), (4.5, 2.5)] )
    