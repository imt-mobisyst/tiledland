# HackaGames UnitTest - `pytest`
import sys, hacka
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Agent, Tile
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_tile_init():
    tile= Tile( shape=Convex().initSquare(1.0) )

    assert tile.id() == 0
    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.body().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
    assert tile.adjacencies() == []
    assert tile.agents() == []
    
    tile= Tile( 3, 0, Convex().initSquare(42.0), Point(10.3, 9.7) )

    assert tile.id() == 3
    assert tile.position().asTuple() == (10.3, 9.7)
    assert tile.body().asZipped() == [(-10.7, -11.3), (-10.7, 30.7), (31.3, 30.7), (31.3, -11.3)]
    assert tile.adjacencies() == []
    assert tile.agents() == []

    tile.setId(1).setGroupAndBrush(8).setPosition(1.0, 1.0)
    tile.setShapeSquare( 2.0 )

    assert tile.id() == 1
    assert tile.group() == 8
    assert tile.position().asTuple() == (1.0, 1.0)
    assert tile.body().asZipped() == [(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]
    assert tile.adjacencies() == []
    assert tile.agents() == []

def test_fast_tile_regular():
    tile= Tile( 1 )
    tile.setPosition(10.0, 10.0)
    tile.setShapeRegular( 20.0, 6 )
    assert tile.id() == 1
    assert tile.position().asTuple() == (10.0, 10.0)
    assert tile.body().size() == 6
    limits= [ ( round(x, 2), round(y, 2) ) for x, y in tile.body().asZipped() ]
    print( limits )
    assert limits == [
        (1.34, 5.0), (1.34, 15.0), (10.0, 20.0),
        (18.66, 15.0), (18.66, 5.0), (10.00, 0.0)
    ]
    
    box= tile.box().round(2)
    assert box.asZip() == [ (1.34, 0.0), (18.66, 20.0) ]
    
def test_fast_tile_adjencies():
    tile= Tile(1)
    assert tile.adjacencies() == []
    tile.connect(2)
    assert tile.adjacencies() == [2]
    tile.connectAll( [3, 4] )
    assert tile.adjacencies() == [2, 3, 4]

def test_fast_tile_str():
    tile= Tile(8)
    tile.setPosition(18.5, 4.07)
    print(f">>> {tile}")
    assert str(tile) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[] agents(0)"
    tile.setGroupAndBrush(2).connectAll( [1, 2, 3] )
    print(f">>> {tile}")
    assert str(tile) == "Tile-2.8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 2, 3] agents(0)"

    tile= Tile( shape= Convex() )
    print(f">>> {tile}")
    assert str(tile) == "Tile-0 ⌊(0.0, 0.0), (0.0, 0.0)⌉ adjs[] agents(0)"

    print(f">>> {tile.body()}")
    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.body().asZipped() == []

def test_fast_tile_absobj():
    tile= Tile(8)
    tile.setPosition(18.5, 4.07)
    tile.connectAll( [ 1, 3, 7, 19 ] )
    tree= tile.asDataTree()

    assert tree.label() == "Tile"

    assert tree.numberOfDigits() == 6
    assert tree.digits() == [ tile.id(), tile.group() ] + [ 1, 3, 7, 19 ]
    
    assert tree.numberOfValues() == 3
    assert tree.values() == [18.5, 4.07, 0.0]
    
    assert tree.numberOfChildren() == 1
    assert tree.children() == [ tile.referenceShape().asDataTree() ]

    bod= Agent()
    tile.append( bod )
    tree= tile.asDataTree()

    assert tree.numberOfChildren() == 2
    for child in tree.children():
        assert type(child) == hacka.DataTree
    assert tree.children() == [ tile.referenceShape().asDataTree(), bod.asDataTree() ]

    tileBis= Tile().fromDataTree( tree )

    assert type( tileBis.agent(1) ) is Agent
    assert not ( tileBis.agent(1) is bod )

    print( tileBis )
    dt= tileBis.asDataTree()

    assert dt.label() == "Tile"

    assert dt.numberOfDigits() == 6
    assert dt.digits() == [ tile.id(), tile.group() ] + [ 1, 3, 7, 19 ]
    
    assert dt.numberOfValues() == 3
    assert dt.values() == [18.5, 4.07, 0.0]
    
    assert dt.numberOfChildren() == 2
    assert dt.children() == [ tile.referenceShape().asDataTree(), bod.asDataTree() ]


def test_fast_tile_DataTreeCopy():
    tile= Tile(8)
    tile.setPosition(18.5, 4.07)
    tile.connectAll( [ 1, 3, 7, 19 ] )
    tile.append( Agent(1) )

    assert tile.adjacencies() == [ 1, 3, 7, 19 ]

    tileBis= tile.dataTreeCopy()
    tile.connect(4)

    assert type(tile) == type(tileBis)
    assert tileBis.adjacencies() == [ 1, 3, 7, 19 ]

    assert str(tileBis) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 3, 7, 19] agents(1)"
    assert str(tileBis.agent()) == str(tile.agent())


def test_fast_tile_clockDirection():
    tile= Tile( shape=Convex().initRegular( 0.2, 12 ) )

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
    tile= Tile( shape=Convex().initRegular( 0.2, 12 ) )
    tile.setPosition(p.x(), p.y())
    
    assert tile.clockDirection( p ) == 0
    assert tile.clockDirection( p + Point(  0.0,  2.0 ) ) == 12
    assert tile.clockDirection( p + Point(  2.0,  0.0 ) ) == 3
    assert tile.clockDirection( p + Point(  0.0, -2.0 ) ) == 6
    assert tile.clockDirection( p + Point( -2.0,  0.0 ) ) == 9
