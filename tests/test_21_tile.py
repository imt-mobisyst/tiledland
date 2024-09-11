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

def test_Tile_copy():
    model= til.Tile().setFromCoordinates( [Coord2(1, 2), Coord2(2, 6), Coord2(4, 5), Coord2(3, 0)] )
    tile= model.copy()

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

def test_Tile_modifier():
    tile= til.Tile().setFromCoordinates( [Coord2(1, 3), Coord2(3, 3), Coord2(3, 1), Coord2(1, 1)] )
    
    assert( tile.center() == Coord2(2.0, 2.0) )

    tileBis= tile.moveTo( Coord2(12.0, -8.0) )

    assert( tileBis == tile )
    assert( tile.size() == 4 )

    print( f"> {tile.center()}" )

    assert( tile.center() == Coord2(12.0, -8.0) )

    assert(
        tile.segment(0) ==  Segment( Coord2(11, -7), Coord2(13, -7) )
    )
    assert(
        tile.segment(1) ==  Segment( Coord2(13, -7), Coord2(13, -9) )
    )
    assert(
        tile.segment(2) ==  Segment( Coord2(13, -9), Coord2(11, -9) )
    )
    assert(
        tile.segment(3) == Segment( Coord2(11, -9), Coord2(11, -7) )
    )