# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Float2, Shape, Body, Tile

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #


def test_Tile_init():
    
    tile= Tile()

    assert tile.id() == 0
    assert tile.matter() == 0
    assert tile.position().tuple() == (0.0, 0.0)
    assert tile.envelope() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    assert tile.adjacencies() == []
    assert tile.bodies() == []
    
    tile= Tile( 3, Float2(10.3, 9.7), Shape(42.0), 0 )

    assert tile.id() == 3
    assert tile.position().tuple() == (10.3, 9.7)
    assert tile.envelope() == [(-10.7, 30.7), (31.3, 30.7), (31.3, -11.3), (-10.7, -11.3)]
    assert tile.adjacencies() == []
    assert tile.bodies() == []

    tile.setId(1).setMatter(8).setPosition( Float2(1.0, 1.0) )
    tile.shape().setShapeSquare( 2.0 )

    assert tile.id() == 1
    assert tile.matter() == 8
    assert tile.position().tuple() == (1.0, 1.0)
    assert tile.envelope() == [(0.0, 2.0), (2.0, 2.0), (2.0, 0.0), (0.0, 0.0)]
    assert tile.adjacencies() == []
    assert tile.bodies() == []

def test_Tile_regular():
    tile= Tile( 1 )
    tile.position().set(10.0, 10.0)
    tile.shape().setShapeRegular( 20.0, 6 )
    assert tile.id() == 1
    assert tile.position().tuple() == (10.0, 10.0)
    assert len(tile.envelope()) == 6
    limits= [ ( round(x, 2), round(y, 2) ) for x, y in tile.envelope() ]
    assert limits == [
        (1.34, 15.0), (10.0, 20.0),
        (18.66, 15.0), (18.66, 5.0),
        (10.00, 0.0), (1.34, 5.0)]
    
    box= tile.box().round(2)
    assert box.zip() == [ (1.34, 0.0), (18.66, 20.0) ]
    
def test_Tile_adjencies():
    tile= Tile(1)
    assert tile.adjacencies() == []
    tile.connect( 2 )
    assert tile.adjacencies() == [2]
    tile.connectAll( [3, 4] )
    assert tile.adjacencies() == [2, 3, 4]

def test_Tile_str():
    tile= Tile(8, Float2(18.5, 4.07))
    print(f">>> {tile}")
    assert str(tile) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[] bodies(0)"
    tile.setMatter(2).connectAll( [1, 2, 3] )
    print(f">>> {tile}")
    assert str(tile) == "Tile-8 ⌊(18.0, 3.57), (19.0, 4.57)⌉ adjs[1, 2, 3] bodies(0)"
