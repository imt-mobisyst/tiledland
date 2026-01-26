# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Point, Line

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G E O M E T R Y
# ------------------------------------------------------------------------ #

def test_line_line():
    l1= Line( Point(1.0, 1.5), Point(7.0, 3.5) )
    l2= Line( Point(5.0, 1.0), Point(3.0, 4.0) )
    boom= Point()

    assert l1.isColliding(l2, boom)
    print( f"Boom: {boom}" )
    assert boom.asTuple() == (4.0, 2.5)
    assert l2.isColliding(l1, boom)
    print( f"Boom: {boom}" )
    assert boom.asTuple() == (4.0, 2.5)

    l1= Line( Point(1.0, 2), Point(7.0, 2) )
    assert l1.isColliding(l2, boom)

    l2= Line( Point(5.0, 1.0), Point(3.0, 1.0) )
    assert not l1.isColliding(l2, boom)
    print( f"Boom: {boom}" )
    
    l1= Line( Point(1.5, 1.5), Point(2.0, 4.0) )
    l2= Line( Point(2.0, 1.0), Point(6.0, 0.5) )
    collide= l1.isColliding(l2, boom)
    print( f"Boom: {boom}" )
    assert not collide
    
    l1= Line( Point(0, 0), Point(0, 4.0) )
    l2= Line( Point(6.0, 0.5), Point(1.0, 1.0) )
    collide= l1.isColliding(l2, boom)
    print( f"Boom: {boom}" )
    assert not collide
    
def test_point_projection():
    p= Point(1.0, 8.0)
    l= Line( Point(0, 0), Point(12, 8) )

    proj= l.projectionPoint(p)
    proj.round(3)
    print(proj)

    assert proj.asTuple() == (4.385, 2.923)

def test_linePoint_distance():
    p= Point(1.0, 8.0)
    l= Line( Point(0, 0), Point(12, 8) )

    dist= l.distancePoint(p)

    assert round(dist, 3) == 6.102
