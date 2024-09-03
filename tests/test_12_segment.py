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
