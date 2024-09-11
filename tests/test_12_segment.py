import sys
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#     T E S T  T i l e d L a n d : :  G e o m t r y : : S e g m e n t      #
# ------------------------------------------------------------------------ #

import src.tiledLand.geometry as tlg

def test_Segment_init1():
    seg= tlg.Segment()
    assert( type(seg) == tlg.Segment )
    assert( seg.dimention() == 2 )
    assert( seg.a().tuple() == (0.0, 0.0) )
    assert( seg.b().tuple() == (0.0, 0.0) )

def test_Segment_init2():
    seg= tlg.Segment(
        tlg.Coord2(23.9, -16.08),
        tlg.Coord2(12.0,  1.302)
    )
    assert( type(seg) == tlg.Segment )
    assert( seg.dimention() == 2 )
    assert( seg.a().tuple() == (23.9, -16.08) )
    assert( seg.b().tuple() == (12.0,  1.302) )

    assert( seg.middle().round().tuple() == (17.9, -7.4) )

def test_Segment_inflate():
    seg= tlg.Segment(
        tlg.Coord2(1.0, 1.0),
        tlg.Coord2(10.0,  1.0)
    )

    assert( seg.vector() == tlg.Coord2(9.0, 0.0) )

    assert( type(seg) == tlg.Segment )
    rectangle= seg.inflate()
    assert( len( rectangle ) == 4 )
    assert( rectangle == [
        tlg.Coord2(1.0, 0.5), tlg.Coord2(1.0, 1.5),
        tlg.Coord2(10.0, 1.5), tlg.Coord2(10.0, 0.5)
    ])

    seg= tlg.Segment(
        tlg.Coord2(1.0, 1.0),
        tlg.Coord2(10.0,  10.0)
    )

    assert( seg.vector() == tlg.Coord2(9.0, 9.0) )
    assert( seg.vector().normal().round(2) == tlg.Coord2(0.71, 0.71) )
    assert( seg.vector().orthonormal().round(2) == tlg.Coord2(-0.71, 0.71) )

    assert( type(seg) == tlg.Segment )
    rectangle= seg.inflate()
    assert( len( rectangle ) == 4 )

    rectangle= [ coord.round(2) for coord in rectangle ]
    print( ", ".join( [str(r) for r in rectangle] ) )

    assert( rectangle == [
        tlg.Coord2(1.35, 0.65), tlg.Coord2(0.65, 1.35),
        tlg.Coord2(9.65, 10.35), tlg.Coord2(10.35, 9.65)
    ])