import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T   M a r a u B o t M a p : :  B O D Y                  #
# ------------------------------------------------------------------------ #
from src.pyConvexMap import Point2

def test_Point2_init():
    p1= Point2()
    assert( type(p1) == Point2 )
    assert( p1.x == 0.0 )
    assert( p1.y == 0.0 )
    assert( p1.tuple() == (0.0, 0.0) )

def test_Point2_init2():
    p1= Point2( 10.4, 3.3 )
    assert( type(p1) == Point2 )
    assert( p1.x == 10.4 )
    assert( p1.y == 3.3 )
    assert( p1.tuple() == (10.4, 3.3) )

    p1= Point2( -0.4, 3.3 )
    assert( type(p1) == Point2 )
    assert( p1.x == -0.4 )
    assert( p1.y == 3.3 )
    assert( p1.tuple() == (-0.4, 3.3) )

def test_Point2_construction():
    pose= Point2( 10.4, 3.3 )
    assert( pose.tuple() == (10.4, 3.3) )

    pose.set( 0.001, -23.1 )
    assert( pose.tuple() == (0.001, -23.1) )

def test_Point2_Comparison():
    point= Point2( 10.4, 0.0 )
    assert( point == Point2( 10.4, 0.0 ) )
    assert( not point == Point2( 10.2, 0.0 ) )
    assert( not point == Point2( 10.4, -0.01 ) )

def test_Point2_Operation():
    point= Point2( 10.4, 0.0 ) + Point2( 1.4, 8.0 )
    assert( point == Point2( 11.8, 8.0 ) )

def test_Point2_distance():
    p1= Point2( 10.4, 0.0 )
    p2= Point2( 1.0, 1.0 )
    
    assert( p1.lenghtSquare() == 10.4*10.4 )
    assert( p1.lenght() ==  10.4 )

    assert( p2.lenghtSquare() == 2 )
    assert( p2.lenght() ==  math.sqrt(2) )

    assert( round( p1.distance( p2 ), 6 ) == 9.453042 )
    assert( round( p2.distance( p1 ), 6 ) == 9.453042 )

    assert( round( p1.distanceSquare( p2 ), 6 ) == 89.36 )
    assert( round( p1.distanceSquare( p1 ), 6 ) == 0.0 )
