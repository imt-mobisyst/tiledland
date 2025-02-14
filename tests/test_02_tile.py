# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from hacka.py  import Pod
from src.tiledland import Float2, Tile

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #


def test_Tile_init():
    
    tile= Tile()

    assert tile.number() == 0
    assert tile.matter() == 0
    assert tile.center().tuple() == (0.0, 0.0)
    assert tile.envelope() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    assert tile.adjacencies() == []
    assert tile.pieces() == []
    
    tile= Tile( 3, 0, Float2(10.3, 9.7), 42.0 )

    assert tile.number() == 3
    assert tile.center().tuple() == (10.3, 9.7)
    assert tile.envelope() == [(-10.7, 30.7), (31.3, 30.7), (31.3, -11.3), (-10.7, -11.3)]
    assert tile.adjacencies() == []
    assert tile.pieces() == []

    tile.setNumber(1).setMatter(8).setCenter(1.0, 1.0).setShapeSquare( 2.0 )

    assert tile.number() == 1
    assert tile.matter() == 8
    assert tile.center().tuple() == (1.0, 1.0)
    assert tile.envelope() == [(0.0, 2.0), (2.0, 2.0), (2.0, 0.0), (0.0, 0.0)]
    assert tile.adjacencies() == []
    assert tile.pieces() == []

def test_Tile_regular():
    tile= Tile( 1 ).setCenter(10.0, 10.0).setShapeRegular( 20.0, 6 )
    assert tile.number() == 1
    assert tile.center().tuple() == (10.0, 10.0)
    assert len(tile.envelope()) == 6
    limits= [ ( round(x, 2), round(y, 2) ) for x, y in tile.envelope() ]
    assert limits == [
        (1.34, 15.0), (10.0, 20.0),
        (18.66, 15.0), (18.66, 5.0),
        (10.00, 0.0), (1.34, 5.0)]
    
    box= [ (round(p.x(), 2), round(p.y(), 2)) for p in tile.box() ]
    assert box == [ (1.34, 0.0), (18.66, 20.0) ]
    
def test_Tile_adjencies():
    tile= Tile(1)
    assert tile.adjacencies() == []
    tile.connect( 2 )
    assert tile.adjacencies() == [2]
    tile.connectAll( [3, 4] )
    assert tile.adjacencies() == [2, 3, 4]

def test_Tile_pieces():
    tile= Tile(1)
    assert tile.pieces() == []
    
    tile.append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    assert len(tile.pieces()) == 1
    assert tile.piece(1) == Pod('Piece', 'dragon', [10, 3], [22.0])
    
    tile.clear()
    assert tile.pieces() == []

def test_Tile_str():
    tile= Tile(8, 0, Float2(18.5, 4.07))
    print(f">>> {tile}")
    assert str(tile) == "Tile-8/0 center: (18.5, 4.07) adjs: [] pieces(0)"
    tile.setMatter(2).connectAll( [1, 2, 3] )
    print(f">>> {tile}")
    assert str(tile) == "Tile-8/2 center: (18.5, 4.07) adjs: [1, 2, 3] pieces(0)"

def test_Tile_pod():
    tile= Tile( 3, 0, Float2(1.0, 2.0), 2.0 )
    tile._adjacencies= [1, 2, 4]
    print( tile.envelope() )
    assert tile.envelope() == [(0.0, 3.0), (2.0, 3.0), (2.0, 1.0), (0.0, 1.0)]    
    
    pod= tile.asPod()
    print(f">>> {pod}")
    
    assert str(pod) == "Tile: [3, 0, 1, 2, 4] [1.0, 2.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0]"
    
    tileBis= Tile().fromPod(pod)
    assert tileBis.number() == 3
    assert tileBis.center().tuple() == (1.0, 2.0)
    assert tile.envelope() == [(0.0, 3.0), (2.0, 3.0), (2.0, 1.0), (0.0, 1.0)]
    assert tileBis.adjacencies() == [1, 2, 4]
    assert tileBis.asPod() == tile.asPod()

def test_Tile_load():
    tile= Tile( 3, 9, Float2(1.4, 2.0), 1.0 )
    assert tile.matter() == 9
    tile.connectAll( [1, 2, 4] )
    tileBis= Tile().load( tile.dump() )
    print( tile )
    print( tileBis )
    assert tileBis.asPod() == tile.asPod()
