import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T   M a r a u B o t M a p : :  B O D Y                  #
# ------------------------------------------------------------------------ #
from src.pyConvexMap import Body2

def test_Body2_init():
    p1= Body2()
    assert( type(p1) == Body2 )
    assert( p1.px == 0.0 )
    assert( p1.py == 0.0 )
    assert( p1.oz == 0.0 )
    assert( p1.tuple() == (0.0, 0.0, 0.0) )
    assert( p1.position() == (0.0, 0.0) )
    assert( p1.orientation() == (0.0) )

def test_Body2_init2():
    p1= Body2( 10.4, 3.3, 1.4 )
    assert( type(p1) == Body2 )
    assert( p1.px == 10.4 )
    assert( p1.py == 3.3 )
    assert( p1.oz == 1.4 )
    assert( p1.tuple() == (10.4, 3.3, 1.4) )
    assert( p1.position() == (10.4, 3.3) )
    assert( p1.orientation() == (1.4) )

    p1= Body2( -0.4, 3.3, -4.28 )
    assert( type(p1) == Body2 )
    assert( p1.px == -0.4 )
    assert( p1.py == 3.3 )
    assert( p1.oz == -4.28 )
    assert( p1.tuple() == (-0.4, 3.3, -4.28) )
    assert( p1.position() == (-0.4, 3.3) )
    assert( p1.orientation() == (-4.28) )

def test_Body2_construction():
    pose= Body2( 10.4, 3.3, 1.4 )
    assert( pose.position() == (10.4, 3.3) )
    assert( pose.orientation() == (1.4) )

    pose.setPosition( 0.001, -23.1 )
    assert( pose.position() == (0.001, -23.1) )
    assert( pose.orientation() == (1.4) )

    pose.setOrientation( -0.1 )
    assert( pose.position() == (0.001, -23.1) )
    assert( pose.orientation() == (-0.1) )

def test_Body2_distance():
    p1= Body2( 10.4, 0.0, 3.0 )
    p2= Body2( 1.0, 1.0, -1.2 )
    
    assert( p1.lenghtSquare() == 10.4*10.4 )
    assert( p1.lenght() ==  10.4 )

    assert( p2.lenghtSquare() == 2 )
    assert( p2.lenght() ==  math.sqrt(2) )

    assert( round( p1.distance( p2 ), 6 ) == 9.453042 )
    assert( round( p2.distance( p1 ), 6 ) == 9.453042 )

    assert( round( p1.distanceSquare( p2 ), 6 ) == 89.36 )
    assert( round( p1.distanceSquare( p1 ), 6 ) == 0.0 )

def test_Body2_move():
    pose= Body2( 10.4, -3.3, 0.0 )
    assert( pose.position() == (10.4, -3.3) )
    assert( pose.orientation() == (0.0) )
    transform= Body2()

    pose.move( transform, dtime=1.0 )
    assert( pose.position() == (10.4, -3.3) )
    assert( pose.orientation() == (0.0) )

    transform.setPosition( -1.0, 0.0 )

    pose.move( transform, dtime=1.0 )
    assert( pose.position() == (9.4, -3.3) )
    assert( pose.orientation() == (0.0) )

    pose.move( transform, dtime=0.5 )
    assert( pose.position() == (8.9, -3.3) )
    assert( pose.orientation() == (0.0) )

    transform.setOrientation( 0.5 )

    pose.move( transform, dtime=1.0 )
    assert( pose.position() == (7.9, -3.3) )
    assert( pose.orientation() == (0.5) )

    pose.move( transform, dtime=0.5 )

    assert( pose.distance( Body2(7.4612, -3.5397) ) < 0.0001 )
    assert( pose.orientation() == (0.75) )
