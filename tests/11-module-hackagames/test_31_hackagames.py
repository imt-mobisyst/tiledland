import src.tiledland as tild

'''
def test_Convex_pod():
    shape= tild.Convex(8, 10.0)
    
    pod= hk.Pod().initFrom( shape )
    print(f">>> {pod}")
    
    assert str(pod) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

    shapeBis= tild.Convex().initFrom(pod)
    
    podBis= hk.Pod().initFrom( shapeBis )
    print(f">>> {podBis}")

    assert str(podBis) == "Convex: [8] [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]"

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

def test_Tabletop_pod():
    tabletop= Tabletop().initLine(4)
    tabletop.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    tabletop.tile(1).setCenter( 5.0, 3.0 )
    tabletop.tile(2).setCenter( 5.0, 15.0 )
    tabletop.tile(3).setCenter( 1.0, 9.0 )
    tabletop.tile(4).setCenter( 9.0, 9.0 )
    
    tabletopPod= tabletop.asDataTree()
    print(f">>>1 {tabletopPod}")
    assert '\n'+ str(tabletopPod) +'\n' == """
Tabletop:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    tabletopPod= Tabletop().fromDataTree( tabletop.asDataTree() ).asDataTree()
    print(f">>>2 {tabletopPod}")
    assert '\n'+ str(tabletopPod) +'\n' == """
Tabletop:
- Convex: [0] [-0.25, 0.1, -0.1, 0.25, 0.1, 0.25, 0.25, 0.1, 0.25, -0.1, 0.1, -0.25, -0.1, -0.25, -0.25, -0.1]
- Tile: [1, 0, 2, 3, 4] [5.0, 3.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [2, 0, 1, 3, 4] [5.0, 15.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [3, 0, 1, 2] [1.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- Tile: [4, 0, 1, 2] [9.0, 9.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
"""

    print(f">>> {tabletopPod.dump()}")
    assert '\n'+ tabletopPod.dump() +'\n' == """
Tabletop - 0 0 0 5 :
Convex - 0 1 16 0 : 0 -0.25 0.1 -0.1 0.25 0.1 0.25 0.25 0.1 0.25 -0.1 0.1 -0.25 -0.1 -0.25 -0.25 -0.1
Tile - 0 5 10 0 : 1 0 2 3 4 5.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 2 0 1 3 4 5.0 15.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 3 0 1 2 1.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 4 0 1 2 9.0 9.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
"""

'''