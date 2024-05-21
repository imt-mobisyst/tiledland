import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T   M a r a u B o t M a p : :  B O D Y                  #
# ------------------------------------------------------------------------ #
from src.pyConvexMap import Point2, Cell


def test_Cell_init():
    cell= Cell()
    assert( type(cell) == Cell )
    assert( cell.center() == Point2(0.0, 0.0) )

def test_Cell_init2():
    cell= Cell( [Point2(1, 2), Point2(2, 6), Point2(4, 5), Point2(3, 0)] )
    assert( type(cell) == Cell )
    assert( cell.limits() == [Point2(1, 2), Point2(2, 6), Point2(4, 5), Point2(3, 0)] )