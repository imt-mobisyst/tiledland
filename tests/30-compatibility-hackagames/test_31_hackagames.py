import src.tiledland as tll

'''
def test_Convex_pod():
    shape= tll.Convex(8, 10.0)
    
    pod= hk.Pod().initializeFrom( shape )
    print(f">>> {pod}")
    
    assert str(pod) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

    shapeBis= tll.Convex().initializeFrom(pod)
    
    podBis= hk.Pod().initializeFrom( shapeBis )
    print(f">>> {podBis}")

    assert str(podBis) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

def test_Tile_pod():
    tile= Tile( 3, 0, Point(1.0, 2.0), 2.0 )
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
    tile= Tile( 3, 9, Point(1.4, 2.0), 1.0 )
    assert tile.matter() == 9
    tile.connectAll( [1, 2, 4] )
    tileBis= Tile().load( tile.dump() )
    print( tile )
    print( tileBis )
    assert tileBis.asPod() == tile.asPod()
    
def test_Tile_load():
    shape= Convex(8).initializeRegular( 12.0, 7 )
    
    shapeBis= Convex().load( shape.dump() )
    print( shape )
    print( shapeBis )
    assert shapeBis.asPod() == shape.asPod()

def test_Tile_agents():
    tile= Tile(1)
    assert tile.agents() == []
    
    tile.append( Pod('Piece', 'dragon', [10, 3], [22.0]) )

    assert len(tile.agents()) == 1
    assert tile.piece(1) == Pod('Piece', 'dragon', [10, 3], [22.0])
    
    tile.clear()
    assert tile.agents() == []

def test_Scene_pod():
    scene= Scene().initializeLine(4)
    scene.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    scene.tile(1).setCenter( 5.0, 3.0 )
    scene.tile(2).setCenter( 5.0, 15.0 )
    scene.tile(3).setCenter( 1.0, 9.0 )
    scene.tile(4).setCenter( 9.0, 9.0 )
    
    scenePod= scene.asPod()
    print(f">>>1 {scenePod}")
    assert '\n'+ str(scenePod) +'\n' == """
Scene:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    scenePod= Scene().fromPod( scene.asPod() ).asPod()
    print(f">>>2 {scenePod}")
    assert '\n'+ str(scenePod) +'\n' == """
Scene:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    print(f">>> {scenePod.dump()}")
    assert '\n'+ scenePod.dump() +'\n' == """
Scene - 0 0 0 5 :
Convex - 0 1 16 0 : 0 -0.25 0.1 -0.1 0.25 0.1 0.25 0.25 0.1 0.25 -0.1 0.1 -0.25 -0.1 -0.25 -0.25 -0.1
Tile - 0 5 10 0 : 1 0 2 3 4 5.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 2 0 1 3 4 5.0 15.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 3 0 1 2 1.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 4 0 1 2 9.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
"""

'''