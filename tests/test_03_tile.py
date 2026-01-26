# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Agent, Tile
from src.tiledland.pod import Pod
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Tile_init():
    tile= Tile( shape=Convex().initializeSquare(1.0) )

    assert tile.id() == 0
    assert tile.matter() == 0
    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.envelope().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
    assert tile.adjacencies() == []
    assert tile.agents() == []
    
    tile= Tile( 3, Point(10.3, 9.7), Convex().initializeSquare(42.0), 0 )

    assert tile.id() == 3
    assert tile.position().asTuple() == (10.3, 9.7)
    assert tile.envelope().asZipped() == [(-10.7, -11.3), (-10.7, 30.7), (31.3, 30.7), (31.3, -11.3)]
    assert tile.adjacencies() == []
    assert tile.agents() == []

    tile.setId(1).setMatter(8).setPosition( Point(1.0, 1.0) )
    tile.shape().initializeSquare( 2.0 )

    assert tile.id() == 1
    assert tile.matter() == 8
    assert tile.position().asTuple() == (1.0, 1.0)
    assert tile.envelope().asZipped() == [(0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0)]
    assert tile.adjacencies() == []
    assert tile.agents() == []

def test_Tile_regular():
    tile= Tile( 1 )
    tile.position().set(10.0, 10.0)
    tile.shape().initializeRegular( 20.0, 6 )
    assert tile.id() == 1
    assert tile.position().asTuple() == (10.0, 10.0)
    assert tile.envelope().size() == 6
    limits= [ ( round(x, 2), round(y, 2) ) for x, y in tile.envelope().asZipped() ]
    assert limits == [
        (1.34, 15.0), (10.0, 20.0),
        (18.66, 15.0), (18.66, 5.0),
        (10.00, 0.0), (1.34, 5.0)]
    
    box= tile.box().round(2)
    assert box.asZip() == [ (1.34, 0.0), (18.66, 20.0) ]
    
def test_Tile_adjencies():
    tile= Tile(1)
    assert tile.adjacencies() == []
    tile.connect( 2 )
    assert tile.adjacencies() == [2]
    tile.connectAll( [3, 4] )
    assert tile.adjacencies() == [2, 3, 4]

def test_Tile_str():
    tile= Tile(8, Point(18.5, 4.07) )
    print(f">>> {tile}")
    assert str(tile) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[] agents(0)"
    tile.setMatter(2).connectAll( [1, 2, 3] )
    print(f">>> {tile}")
    assert str(tile) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 2, 3] agents(0)"

    tile= Tile( shape= Convex() )
    print(f">>> {tile}")
    assert str(tile) == "Tile-0 ⌊(0.0, 0.0), (0.0, 0.0)⌉ adjs[] agents(0)"

    print(f">>> {tile.envelope()}")
    assert tile.position().asTuple() == (0.0, 0.0)
    assert tile.envelope().asZipped() == []

def test_Tile_absobj():
    tile= Tile(8, Point(18.5, 4.07))
    tile.connectAll( [ 1, 3, 7, 19 ] )
    pod= tile.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Tile"]
    assert pod.word() == "Tile"

    assert pod.numberOfIntegers() == 6
    assert pod.integers() == [ tile.id(), tile.matter() ] + [ 1, 3, 7, 19 ]
    
    assert pod.numberOfValues() == 2
    assert pod.values() == [18.5, 4.07]
    
    assert pod.numberOfChildren() == 1
    assert pod.children() == [ tile.shape().asPod() ]

    bod= Agent()
    tile.append( bod )
    pod= tile.asPod()

    assert pod.numberOfChildren() == 2
    for child in pod.children():
        assert type(child) == Pod
    assert pod.children() == [ tile.shape().asPod(), bod.asPod() ]

    tileBis= Tile().fromPod( pod )

    assert type( tileBis.agent(1) ) is Agent
    assert not ( tileBis.agent(1) is bod )

    print( tileBis )
    pod= tileBis.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Tile"]
    assert pod.word() == "Tile"

    assert pod.numberOfIntegers() == 6
    assert pod.integers() == [ tile.id(), tile.matter() ] + [ 1, 3, 7, 19 ]
    
    assert pod.numberOfValues() == 2
    assert pod.values() == [18.5, 4.07]
    
    assert pod.numberOfChildren() == 2
    assert pod.children() == [ tile.shape().asPod(), bod.asPod() ]


def test_Tile_podCopy():
    tile= Tile(8, Point(18.5, 4.07))
    tile.connectAll( [ 1, 3, 7, 19 ] )
    tile.append( Agent(1) )

    assert tile.adjacencies() == [ 1, 3, 7, 19 ]

    tileBis= tile.podCopy()
    tile.connect(4)

    assert type(tile) == type(tileBis)
    assert tileBis.adjacencies() == [ 1, 3, 7, 19 ]

    assert str(tileBis) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 3, 7, 19] agents(1)"
    assert str(tileBis.agent()) == str(tile.agent())


def test_Tile_clockDirection():
    tile= Tile( shape=Convex().initializeRegular( 0.2, 12 ) )

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
    tile= Tile( position=p, shape=Convex().initializeRegular( 0.2, 12 ) )

    assert tile.clockDirection( p ) == 0
    assert tile.clockDirection( p + Point(  0.0,  2.0 ) ) == 12
    assert tile.clockDirection( p + Point(  2.0,  0.0 ) ) == 3
    assert tile.clockDirection( p + Point(  0.0, -2.0 ) ) == 6
    assert tile.clockDirection( p + Point( -2.0,  0.0 ) ) == 9
