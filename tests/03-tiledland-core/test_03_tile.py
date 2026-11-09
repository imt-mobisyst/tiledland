# HackaGames UnitTest - `pytest`
import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Unit, Tile, artist
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_tile_init():
    tile= Tile( Convex().initSquare(1.0) )

    assert type( tile ) == Tile

    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.orientation() == 0.0
    assert str(tile.box()) == "⌊(-0.5, -0.5), (0.5, 0.5)⌉"
    assert tile.radius() ==  math.sqrt(0.5)
    assert str( tile.shape().asRoundZipped() ) == "[(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]"
    assert tile.shape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert tile.isValidShaped()

    assert tile.owner() == 0
    assert tile.category() == 0
    assert tile.index() == 0
    assert tile.adjacencies() == []
    assert tile.units() == []
    
    tile= Tile( Convex().initSquare(42.0) ).setIndex(3)
    tile.setPosition( Point(10.3, 9.7) )

    assert tile.index() == 3
    assert tile.position().asTuple() == (10.3, 9.7)
    assert tile.shape().asZipped() == [(-10.7, -11.3), (-10.7, 30.7), (31.3, 30.7), (31.3, -11.3)]
    assert tile.adjacencies() == []
    assert tile.units() == []

    tile.setShape( Convex().initSquare(2.0) )
    tile.setIndex(1).setPosition( Point(1.0, 1.0) )
    
    assert tile.index() == 1
    assert tile.position().asTuple() == (1.0, 1.0)
    assert tile.shape().asZipped() == [(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]
    assert tile.adjacencies() == []
    assert tile.units() == []

def test_fast_tile_regular():
    tile= Tile( index= 1)
    tile.setShape( Convex().initRegular(20.0, 6) )
    tile.setPosition( Point(10.0, 10.0) )

    assert tile.index() == 1
    assert tile.position().asTuple() == (10.0, 10.0)
    assert tile.shape().size() == 6
    limits= [ ( round(x, 2), round(y, 2) ) for x, y in tile.shape().asZipped() ]
    print( limits )
    assert limits == [
        (1.34, 5.0), (1.34, 15.0), (10.0, 20.0),
        (18.66, 15.0), (18.66, 5.0), (10.00, 0.0)
    ]
    
    box= tile.box().round(2)
    assert box.asZip() == [ (1.34, 0.0), (18.66, 20.0) ]
    
def test_fast_tile_adjencies():
    tile= Tile( index= 1)
    assert tile.adjacencies() == []
    tile.connect(2)
    assert tile.adjacencies() == [2]
    tile.connectAll( [3, 4] )
    assert tile.adjacencies() == [2, 3, 4]

def test_fast_tile_str():
    tile= Tile( index= 8 )
    tile.setPosition( Point(18.5, 4.07) )
    
    print(f">>> {tile}")
    assert str(tile) == "Tile 0-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[] units(0)"
    
    tile.connectAll( [1, 2, 3] )
    print(f">>> {tile}")
    assert str(tile) == "Tile 0-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 2, 3] units(0)"

    tile= Tile( Convex() )
    print(f">>> {tile}")
    assert str(tile) == "Tile 0-0 ⌊(0.0, 0.0), (0.0, 0.0)⌉ adjs[] units(0)"

    print(f">>> {tile.shape()}")
    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.shape().asZipped() == []

    str(Tile()) == "Tile 0-0 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[] units(0)"
    
def test_fast_tile_clockDirection():
    tile= Tile( Convex().initRegular( 0.2, 12 ) )

    assert tile.clockDirection( Point(  0.0,  0.0 ) ) == 0
    assert tile.clockDirection( Point(  0.0,  1.0 ) ) == 12
    assert tile.clockDirection( Point(  1.0,  0.0 ) ) == 3
    assert tile.clockDirection( Point(  0.0, -1.0 ) ) == 6
    assert tile.clockDirection( Point( -1.0,  0.0 ) ) == 9
    
    assert tile.clockDirection( Point(  0.0,  0.0 ) ) == 0
    assert tile.clockDirection( Point(  0.0,  2.0 ) ) == 12
    assert tile.clockDirection( Point(  2.0,  0.0 ) ) == 3
    assert tile.clockDirection( Point(  0.0, -2.0 ) ) == 6
    assert tile.clockDirection( Point( -2.0,  0.0 ) ) == 9
    
    p= Point( 1.2, -0.5 )
    tile= Tile( Convex().initRegular( 0.2, 12 ) )
    tile.setPosition( Point(p.x(), p.y()) )
    
    assert tile.clockDirection( p ) == 0
    assert tile.clockDirection( p + Point(  0.0,  2.0 ) ) == 12
    assert tile.clockDirection( p + Point(  2.0,  0.0 ) ) == 3
    assert tile.clockDirection( p + Point(  0.0, -2.0 ) ) == 6
    assert tile.clockDirection( p + Point( -2.0,  0.0 ) ) == 9
