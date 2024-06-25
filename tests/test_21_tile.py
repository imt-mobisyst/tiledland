import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T  T i l e d M a p : :  T I L E                  #
# ------------------------------------------------------------------------ #
import src.tiledMap as tim

def test_Tile_init():
    tile= tim.Tile()
    assert( type(tile) == tim.Tile )

def test_Tile_init2():
    tile= tim.Tile( [(1, 2), (2, 6), (4, 5), (3, 0)] )
    assert( type(tile) == tim.Tile )
    assert( tile.segments() == [
        ( (1.0, 2.0), (2.0, 6.0) ),
        ( (2.0, 6.0), (4.0, 5.0) ),
        ( (4.0, 5.0), (3.0, 0.0) ),
        ( (3.0, 0.0), (1.0, 2.0) ),
    ])

    print( shapely.centroid( tile._shape ) )
    print( tile.center() )
    assert( tim.roundPoint( tile.center() ) == (2.5, 3.2) )
    assert( 
        tile.segmentTags() ==
        [ 0, 0, 0, 0 ]
    )

def test_Tile_segement():
    tile= tim.Tile( [(1, 2), (2, 6), (4, 5), (3, 0)] )
    assert( tile.size() == 4 )
    assert(
        tile.segment(0) ==  ((1.0, 2.0), (2.0, 6.0))
    )
    assert(
        tile.segment(1) ==  ((2.0, 6.0), (4.0, 5.0))
    )
    assert(
        tile.segment(2) ==  ((4.0, 5.0), (3.0, 0.0))
    )
    assert(
        tile.segment(3) ==  ((3.0, 0.0), (1.0, 2.0))
    )
