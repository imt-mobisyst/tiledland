import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T   M a r a u B o t M a p : :  B O D Y                  #
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
        tile.segmentTypes() ==
        [ 0, 0, 0, 0 ]
    )
