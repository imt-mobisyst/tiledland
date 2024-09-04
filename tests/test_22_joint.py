import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#               T E S T  T i l e d M a p : :  J O I N T                    #
# ------------------------------------------------------------------------ #
import src.tiledLand as tim
from src.tiledLand.geometry import Coord2, Segment

def test_Joint_init():
    joint= tim.Joint()
    assert( type(joint) == tim.Joint )

def test_Joint_init2():
    joint= tim.Joint(
        tim.Tile().setFromCoordinates( [ Coord2(7.0, 1.0), Coord2(9.0, 1.0), Coord2(9.0, 3.0), Coord2(7.0, 3.0)] ),
        tim.Tile().setFromCoordinates( [ Coord2(7.0, 4.0), Coord2(9.0, 5.0), Coord2(7.0, 6.0)] ),
        0, 2
    )
    assert(
        joint.tileA().segments() == [
            Segment( Coord2(7.0, 1.0), Coord2(9.0, 1.0) ),
            Segment( Coord2(9.0, 1.0), Coord2(9.0, 3.0) ),
            Segment( Coord2(9.0, 3.0), Coord2(7.0, 3.0) ),
            Segment( Coord2(7.0, 3.0), Coord2(7.0, 1.0) ),
    ])
    
    assert( joint.tileB().segments() == [
        Segment( Coord2(7.0, 4.0), Coord2(9.0, 5.0) ),
        Segment( Coord2(9.0, 5.0), Coord2(7.0, 6.0) ),
        Segment( Coord2(7.0, 6.0), Coord2(7.0, 4.0) )
    ])
        
    assert( joint.gates() == ( Segment( Coord2(7.0, 1.0), Coord2(9.0, 1.0) ),
                                Segment( Coord2(7.0, 6.0), Coord2(7.0, 4.0) ) )
    )
    
    assert( joint.shapeSegments() == [
        Segment( Coord2(7.0, 1.0), Coord2(9.0, 1.0) ),
        Segment( Coord2(9.0, 1.0), Coord2(7.0, 6.0) ),
        Segment( Coord2(7.0, 6.0), Coord2(7.0, 4.0) ),
        Segment( Coord2(7.0, 4.0), Coord2(7.0, 1.0) )
    ])

def test_joint_autoSegemntSelection():
    t1= tim.Tile().setFromCoordinates( [ Coord2(3,1), Coord2(5,1), Coord2(5,3), Coord2(3,3)] )
    t2= tim.Tile().setFromCoordinates( [ Coord2(3,4), Coord2(5,4), Coord2(4,6)] )
    joint= tim.Joint( t1, t2 )

    assert( joint._gateA == 0 )
    assert( joint._gateB == 0 )

    assert( joint.updateGates() )
    
    assert( joint._gateA == 2 )
    assert( joint._gateB == 0 )
