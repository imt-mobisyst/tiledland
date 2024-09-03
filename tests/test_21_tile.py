import sys, math, shapely
sys.path.insert( 1, __file__.split('tests')[0] )

# ------------------------------------------------------------------------ #
#            T E S T  T i l e d M a p : :  T I L E                  #
# ------------------------------------------------------------------------ #
import src.tiledLand as til
from src.tiledLand.geometry import Coord2, Segment

def test_Tile_init():
    tile= til.Tile()
    assert( type(tile) == til.Tile )
    assert( tile.size() == 0 )
    assert( tile.segments() == [] )

def test_Tile_init2():
    tile= til.Tile().setFromCoordinates( [ Coord2(1, 2), Coord2(2, 6), Coord2(4, 5), Coord2(3, 0) ] )
    assert( type(tile) == til.Tile )
    assert( tile.segments() == [
        Segment( Coord2(1, 2), Coord2(2, 6) ),
        Segment( Coord2(2, 6), Coord2(4, 5) ),
        Segment( Coord2(4, 5), Coord2(3, 0) ),
        Segment( Coord2(3, 0), Coord2(1, 2) ),
    ])

    assert( tile.center().round() == Coord2(2.5, 3.2) )
    assert( tile.segmentTags() == [ 0, 0, 0, 0 ] )

def test_Tile_segement():
    tile= til.Tile().setFromCoordinates( [Coord2(1, 2), Coord2(2, 6), Coord2(4, 5), Coord2(3, 0)] )
    assert( tile.size() == 4 )
    assert(
        tile.segment(0) ==  Segment( Coord2(1, 2), Coord2(2, 6) )
    )
    assert(
        tile.segment(1) ==  Segment( Coord2(2, 6), Coord2(4, 5) )
    )
    assert(
        tile.segment(2) ==  Segment( Coord2(4, 5), Coord2(3, 0) )
    )
    assert(
        tile.segment(3) == Segment( Coord2(3, 0), Coord2(1, 2) )
    )
