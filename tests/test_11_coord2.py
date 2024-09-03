import sys
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#      T E S T  T i l e d L a n d : :  G e o m t r y : : C o o r d 2       #
# ------------------------------------------------------------------------ #

import src.tiledLand.geometry as tlg

def test_Coord2_init1():
    coord2= tlg.Coord2()
    assert( type(coord2) == tlg.Coord2 )
    assert( coord2.dimention() == 2 )
    assert( coord2.x() == 0.0 )
    assert( coord2.y() == 0.0 )
    assert( coord2.tuple() == (0.0, 0.0) )

def test_Coord2_init2():
    coord2= tlg.Coord2(23.9, -16.08)
    assert( coord2.dimention() == 2 )
    assert( coord2.x() == 23.9 )
    assert( coord2.y() == -16.08 )
    assert( coord2.tuple() == (23.9, -16.08) )

def test_Coord2_operators():
    a= tlg.Coord2(23.2, -16.0)
    b= tlg.Coord2(12.2, -0.1)
    
    ab= b + a
    assert( type(ab) == tlg.Coord2 )
    assert( ab.tuple() == ((35.4, -16.1)) )
    
    ab= b - a
    assert( type(ab) == tlg.Coord2 )
    assert( ab.tuple() == ((-11.0, 15.9)) )

def test_Coord2_comparison():
    a= tlg.Coord2(12.2, -0.1)
    b= tlg.Coord2(12.2, -0.1)

    assert( a == b )

    a.set( 26.6, 3 )
    assert( a != b )
    