import src.tiledland as tll

'''
def test_Convex_pod():
    shape= tll.Convex(8, 10.0)
    
    pod= hk.Pod().initFrom( shape )
    print(f">>> {pod}")
    
    assert str(pod) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

    shapeBis= tll.Convex().initFrom(pod)
    
    podBis= hk.Pod().initFrom( shapeBis )
    print(f">>> {podBis}")

    assert str(podBis) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

def test_Tile_pod():
    tile= Tile( 3, 0, Point(1.0, 2.0), 2.0 )
    tile._adjacencies= [1, 2, 4]
    print( tile.body() )
    assert tile.body() == [(0.0, 3.0), (2.0, 3.0), (2.0, 1.0), (0.0, 1.0)]    
    
    pod= tile.asDataTree()
    print(f">>> {pod}")
    
    assert str(pod) == "Tile: [3, 0, 1, 2, 4] [1.0, 2.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0]"
    
    tileBis= Tile().fromDataTree(pod)
    assert tileBis.id() == 3
    assert tileBis.center().tuple() == (1.0, 2.0)
    assert tile.body() == [(0.0, 3.0), (2.0, 3.0), (2.0, 1.0), (0.0, 1.0)]
    assert tileBis.adjacencies() == [1, 2, 4]
    assert tileBis.asDataTree() == tile.asDataTree()

def test_Tile_load():
    tile= Tile( 3, 9, Point(1.4, 2.0), 1.0 )
    assert tile.matter() == 9
    tile.connectAll( [1, 2, 4] )
    tileBis= Tile().load( tile.dump() )
    print( tile )
    print( tileBis )
    assert tileBis.asDataTree() == tile.asDataTree()
    
def test_Tile_load():
    shape= Convex(8).initRegular( 12.0, 7 )
    
    shapeBis= Convex().load( shape.dump() )
    print( shape )
    print( shapeBis )
    assert shapeBis.asDataTree() == shape.asDataTree()

def test_Tile_agents():
    tile= Tile(1)
    assert tile.agents() == []
    
    tile.append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    assert len(tile.agents()) == 1
    assert tile.piece(1) == Pod('Piece', 'dragon', [10, 3], [22.0])
    
    tile.clear()
    assert tile.agents() == []

def test_Map_pod():
    map= Map().initLine(4)
    map.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    map.tile(1).setCenter( 5.0, 3.0 )
    map.tile(2).setCenter( 5.0, 15.0 )
    map.tile(3).setCenter( 1.0, 9.0 )
    map.tile(4).setCenter( 9.0, 9.0 )
    
    mapPod= map.asDataTree()
    print(f">>>1 {mapPod}")
    assert '\n'+ str(mapPod) +'\n' == """
Map:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    mapPod= Map().fromDataTree( map.asDataTree() ).asDataTree()
    print(f">>>2 {mapPod}")
    assert '\n'+ str(mapPod) +'\n' == """
Map:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    print(f">>> {mapPod.dump()}")
    assert '\n'+ mapPod.dump() +'\n' == """
Map - 0 0 0 5 :
Convex - 0 1 16 0 : 0 -0.25 0.1 -0.1 0.25 0.1 0.25 0.25 0.1 0.25 -0.1 0.1 -0.25 -0.1 -0.25 -0.25 -0.1
Tile - 0 5 10 0 : 1 0 2 3 4 5.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 2 0 1 3 4 5.0 15.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 3 0 1 2 1.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 4 0 1 2 9.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
"""

'''