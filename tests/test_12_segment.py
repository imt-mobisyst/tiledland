import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T                     #
# ------------------------------------------------------------------------ #
from src.pyPolyMap import Point2, Segment


def test_Segment_init():
    seg= Segment()
    assert( type(seg) == Segment )
    assert( seg.pointA() == Point2(0.0, 0.0) )
    assert( seg.pointB() == Point2(0.0, 0.0) )

def test_Segment_init2():
    seg= Segment( Point2(1, 2), Point2(2, 6) )
    assert( type(seg) == Segment )
    assert( seg.pointA() == Point2(1, 2) )
    assert( seg.pointB() == Point2(2, 6) )
    assert( seg.tag() == 0 )
    assert( seg == Segment( Point2(1, 2), Point2(2, 6) ) )
    assert( seg.center() == Point2(1.5, 4) )

    seg= Segment( Point2(2, 6), Point2(1, 2) )
    assert( type(seg) == Segment )
    assert( seg.pointA() == Point2(1, 2) )
    assert( seg.pointB() == Point2(2, 6) )
