import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#               T E S T  T i l e d M a p : :  J O I N T                    #
# ------------------------------------------------------------------------ #
import src.tiledMap as tim

def test_Joint_init():
    joint= tim.Joint()
    assert( type(joint) == tim.Joint )

def test_Joint_init2():
    joint= tim.Joint(
        tim.Tile( [(7.0, 1.0), (9.0, 1.0), (9.0, 3.0), (7.0, 3.0)] ),
        tim.Tile( [(7.0, 4.0), (9.0, 5.0), (7.0, 6.0)] ),
        0, 2
    )
    assert(
        joint.tileA().segments() == [
        ( (7.0, 1.0), (9.0, 1.0) ),
        ( (9.0, 1.0), (9.0, 3.0) ),
        ( (9.0, 3.0), (7.0, 3.0) ),
        ( (7.0, 3.0), (7.0, 1.0) ),
    ])
    
    assert( joint.tileB().segments() == [
        ( (7.0, 4.0), (9.0, 5.0) ),
        ( (9.0, 5.0), (7.0, 6.0) ),
        ( (7.0, 6.0), (7.0, 4.0) )
    ])
        
    assert( joint.segments() == [
        ( (7.0, 1.0), (9.0, 1.0) ),
        ( (9.0, 1.0), (7.0, 6.0) ),
        ( (7.0, 6.0), (7.0, 4.0) ),
        ( (7.0, 4.0), (7.0, 1.0) )
    ])

def test_joint_autoSegemntSelection():
    t1= tim.Tile( [(3,1), (5,1), (5,3), (3,3)] )
    t2= tim.Tile( [(3,4), (5,4), (4,6)] )
    joint= tim.Joint( t1, t2 )

    assert( joint._segmentA == 0 )
    assert( joint._segmentB == 0 )

    assert( joint.updateSegments() )
    
    assert( joint._segmentA == 2 )
    assert( joint._segmentB == 0 )