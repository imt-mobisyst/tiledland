import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T   M a r a u B o t M a p : :  B O D Y                  #
# ------------------------------------------------------------------------ #
from src.pyPolyMap import Body2, Point2

def test_Body2_init():
    p1= Body2()
    assert( type(p1) == Body2 )
    assert( p1.tuple() == (0.0, 0.0, 0.0, 1.0) )
    assert( p1.position.tuple() == (0.0, 0.0) )
    assert( p1.orientation == (0.0) )

def test_Body2_init2():
    p1= Body2( 10.4, 3.3, 1.4 )
    assert( type(p1) == Body2 )
    assert( p1.tuple() == (10.4, 3.3, 1.4, 1.0) )
    assert( p1.position.tuple() == (10.4, 3.3) )
    assert( p1.orientation == (1.4) )

    p1= Body2( -0.4, 3.3, -4.28 )
    assert( type(p1) == Body2 )
    assert( p1.tuple() == (-0.4, 3.3, -4.28, 1.0) )
    assert( p1.position.tuple() == (-0.4, 3.3) )
    assert( p1.orientation == (-4.28) )

def test_Body2_construction():
    pose= Body2( 10.4, 3.3, 1.4 )
    assert( pose.position.tuple() == (10.4, 3.3) )
    assert( pose.orientation == (1.4) )

    pose.setPosition( 0.001, -23.1 )
    assert( pose.position.tuple() == (0.001, -23.1) )
    assert( pose.orientation == (1.4) )

    pose.setOrientation( -0.1 )
    assert( pose.position.tuple() == (0.001, -23.1) )
    assert( pose.orientation == (-0.1) )

def test_Body2_distance():
    p1= Body2( 10.4, 0.0, 3.0 )
    p2= Body2( 1.0, 1.0, -1.2 )
    
    assert( round( p1.distance( p2 ), 6 ) == 9.453042 )
    assert( round( p2.distance( p1 ), 6 ) == 9.453042 )

def test_Body2_move():
    pose= Body2( 10.4, -3.3, 0.0 )
    assert( pose.position.tuple() == (10.4, -3.3) )
    assert( pose.orientation == (0.0) )
    
    trans= Point2()
    rot= 0.0

    pose.move( trans, rot, dtime=1.0 )
    assert( pose.position.tuple() == (10.4, -3.3) )
    assert( pose.orientation == (0.0) )

    trans.set( -1.0, 0.0 )

    pose.move( trans, rot, dtime=1.0 )
    assert( pose.position.tuple() == (9.4, -3.3) )
    assert( pose.orientation == (0.0) )

    pose.move( trans, rot, dtime=0.5 )
    assert( pose.position.tuple() == (8.9, -3.3) )
    assert( pose.orientation == (0.0) )

    rot=  0.5

    pose.move( trans, rot, dtime=1.0 )
    assert( pose.position.tuple() == (7.9, -3.3) )
    assert( pose.orientation == (0.5) )

    pose.move( trans, rot, dtime=0.5 )

    assert( pose.distance( Body2(7.4612, -3.5397) ) < 0.0001 )
    assert( pose.orientation == (0.75) )
