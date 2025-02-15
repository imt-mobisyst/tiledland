import src.tiledland as tll
import hacka.py as hk

'''
def test_Shape_pod():
    shape= tll.Shape(8, 10.0)
    
    pod= hk.Pod().initializeFrom( shape )
    print(f">>> {pod}")
    
    assert str(pod) == "Shape: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

    shapeBis= tll.Shape().initializeFrom(pod)
    
    podBis= hk.Pod().initializeFrom( shapeBis )
    print(f">>> {podBis}")

    assert str(podBis) == "Shape: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

def test_Tile_pod():
    tile= Tile( 3, 0, Float2(1.0, 2.0), 2.0 )
    tile._adjacencies= [1, 2, 4]
    print( tile.envelope() )
    assert tile.envelope() == [(0.0, 3.0), (2.0, 3.0), (2.0, 1.0), (0.0, 1.0)]    
    
    pod= tile.asPod()
    print(f">>> {pod}")
    
    assert str(pod) == "Tile: [3, 0, 1, 2, 4] [1.0, 2.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0]"
    
    tileBis= Tile().fromPod(pod)
    assert tileBis.id() == 3
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
    
def test_Tile_load():
    shape= Shape(8).setShapeRegular( 12.0, 7 )
    
    shapeBis= Shape().load( shape.dump() )
    print( shape )
    print( shapeBis )
    assert shapeBis.asPod() == shape.asPod()

def test_Tile_bodies():
    tile= Tile(1)
    assert tile.bodies() == []
    
    tile.append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    assert len(tile.bodies()) == 1
    assert tile.piece(1) == Pod('Piece', 'dragon', [10, 3], [22.0])
    
    tile.clear()
    assert tile.bodies() == []
'''