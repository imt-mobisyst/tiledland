import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_g2s_makeConvexes_small():
    grid= tll.Grid()
    grid.initialize([
        [1, 1, 0,  0, 0],
        [1, 1, 0,  0, 0],
        [0, 0, 0,  0, 0],

        [0, 0, 0,  0, 0],
        [0, 0, 0,  0, 0],
        [0, 0, 0,  0, 0]
    ])

    assert grid.resolution() == 0.1 # dm
    assert grid.position().asTuple() == (0.0, 0.0)
    shapes= grid.makeConvexes()

    assert len(shapes) == 2
    
    print( shapes[0].round(2).asZipped() )
    assert shapes[0].round(2).asZipped() == [
        (0.01, 0.01), (0.01, 0.39), (0.49, 0.39), (0.49, 0.01)
    ]

    print( shapes[1].round(2).asZipped() )
    assert shapes[1].round(2).asZipped() == [
        (0.21, 0.41), (0.21, 0.59), (0.49, 0.59), (0.49, 0.41)
    ]

    # Scene Construction :
    scene= tll.Scene( epsilon=0.06 )
    shapes= grid.makeConvexes(0)
    i= 0
    for s in shapes :
        i+= 1
        assert scene.createTile(s, 0) == i
        scene.tile(i).position().round(2)
        scene.tile(i).shape().round(2)
    assert scene.size() == i
    assert i == 2

    print( scene.asPod() )
    assert "\n"+ str(scene.asPod()) +"\n" =="""
Scene: [0.06]
- Tile: [1, 0] [0.25, 0.2]
  - Convex: [-0.24, -0.19, -0.24, 0.19, 0.24, 0.19, 0.24, -0.19]
- Tile: [2, 0] [0.35, 0.5]
  - Convex: [-0.14, -0.09, -0.14, 0.09, 0.14, 0.09, 0.14, -0.09]
"""

    shapes= grid.makeConvexes(1)
    for s in shapes :
        i+= 1
        assert scene.createTile(s, 1) == i
        scene.tile(i).position().round(2)
        scene.tile(i).shape().round(2)
    assert scene.size() == 3

    print( '-'*10 )
    print( scene.asPod() )

    assert "\n"+ str(scene.asPod()) +"\n" =="""
Scene: [0.06]
- Tile: [1, 0] [0.25, 0.2]
  - Convex: [-0.24, -0.19, -0.24, 0.19, 0.24, 0.19, 0.24, -0.19]
- Tile: [2, 0] [0.35, 0.5]
  - Convex: [-0.14, -0.09, -0.14, 0.09, 0.14, 0.09, 0.14, -0.09]
- Tile: [3, 1] [0.1, 0.5]
  - Convex: [-0.09, -0.09, -0.09, 0.09, 0.09, 0.09, 0.09, -0.09]
"""

    scene.connectAllClose( grid.resolution() )

    print( '-'*10 )
    print( scene.asPod() )

    assert "\n"+ str(scene.asPod()) +"\n" =="""
Scene: [0.06]
- Tile: [1, 0, 2, 3] [0.25, 0.2]
  - Convex: [-0.24, -0.19, -0.24, 0.19, 0.24, 0.19, 0.24, -0.19]
- Tile: [2, 0, 1, 3] [0.35, 0.5]
  - Convex: [-0.14, -0.09, -0.14, 0.09, 0.14, 0.09, 0.14, -0.09]
- Tile: [3, 1, 1, 2] [0.1, 0.5]
  - Convex: [-0.09, -0.09, -0.09, 0.09, 0.09, 0.09, 0.09, -0.09]
"""

    # Scene Construction, in short:
    scene= tll.Scene().fromGrid(grid)
    scene._epsilon= round( scene._epsilon, 6 )

    for t in scene.tiles() :
        t.position().round(2)
        t.shape().round(2)
    
    print( '-'*10 )
    print( scene.asPod() )

    tll.artist.draw(scene)

    assert True or "\n"+ str(scene.asPod()) +"\n" =="""
Scene: [0.06]
- Tile: [1, 0, 2, 3] [0.25, 0.2]
  - Convex: [-0.24, -0.19, -0.24, 0.19, 0.24, 0.19, 0.24, -0.19]
- Tile: [2, 0, 1, 3] [0.35, 0.5]
  - Convex: [-0.14, -0.09, -0.14, 0.09, 0.14, 0.09, 0.14, -0.09]
- Tile: [3, 1, 1, 2] [0.1, 0.5]
  - Convex: [-0.09, -0.09, -0.09, 0.09, 0.09, 0.09, 0.09, -0.09]
"""

def test_g2s_makeConvexes_medium():
    grid= tll.Grid()
    grid.initialize([
        [1, 1, 1,  0, 0, 0,  0, 0, 0],
        [1, 1, 0,  0, 0, 0,  0, 0, 0],
        [1, 0, 0,  0, 0, 0,  0, 0, 0],

        [0, 0, 0,  0, 1, 1,  0, 0, 0],
        [0, 0, 0,  0, 1, 1,  0, 0, 0],
        [0, 0, 0,  0, 1, 1,  0, 0, 0],

        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  0, 0, 0]
    ])

    shapes= grid.makeConvexes()

    assert len(shapes) == 6
    referes= [
        [(0.01, 0.01), (0.01, 0.59), (0.39, 0.59), (0.39, 0.01)],
        [(0.41, 0.01), (0.41, 0.29), (0.89, 0.29), (0.89, 0.01)],
        [(0.61, 0.31), (0.61, 0.89), (0.89, 0.89), (0.89, 0.31)],
        [(0.11, 0.61), (0.11, 0.69), (0.59, 0.69), (0.59, 0.61)],
        [(0.21, 0.71), (0.21, 0.79), (0.59, 0.79), (0.59, 0.71)],
        [(0.31, 0.81), (0.31, 0.89), (0.59, 0.89), (0.59, 0.81)]
    ]

    print( '-'*10 )
    for shape, ref  in zip( shapes, referes ) :
        print( shape.round(2).asZipped() )
        assert shape.asZipped() ==  ref
    
    shapes= grid.makeConvexes(1)

    assert len(shapes) == 4
    referes= [
        [(0.41, 0.31), (0.41, 0.59), (0.59, 0.59), (0.59, 0.31)],
        [(0.01, 0.61), (0.01, 0.89), (0.09, 0.89), (0.09, 0.61)],
        [(0.11, 0.71), (0.11, 0.89), (0.19, 0.89), (0.19, 0.71)],
        [(0.21, 0.81), (0.21, 0.89), (0.29, 0.89), (0.29, 0.81)]
    ]

    print( '-'*10 )
    for shape, ref  in zip( shapes, referes ) :
        print( shape.round(2).asZipped() )
        assert True or shape.asZipped() ==  ref
    
    # Scene from grid:
    scene= tll.Scene().fromGrid(grid)

    for t in scene.tiles() :
        t.position().round(2)
        t.shape().round(2)
    
    print( '-'*10 )
    print( scene.asPod() )

    tll.artist.draw(scene)

    assert "\n"+ str(scene.asPod()) +"\n" == """
Scene: [0.04000000000000001]
- Tile: [1, 0, 2, 4, 5, 6] [0.2, 0.3]
  - Convex: [-0.19, -0.29, -0.19, 0.29, 0.19, 0.29, 0.19, -0.29]
- Tile: [2, 0, 1, 3, 5] [0.65, 0.15]
  - Convex: [-0.24, -0.14, -0.24, 0.14, 0.24, 0.14, 0.24, -0.14]
- Tile: [3, 0, 2, 4, 5] [0.75, 0.6]
  - Convex: [-0.14, -0.29, -0.14, 0.29, 0.14, 0.29, 0.14, -0.29]
- Tile: [4, 0, 1, 3, 5, 6] [0.35, 0.75]
  - Convex: [-0.24, -0.14, -0.24, -0.06, -0.04, 0.14, 0.24, 0.14, 0.24, -0.14]
- Tile: [5, 1, 1, 2, 3, 4] [0.5, 0.45]
  - Convex: [-0.09, -0.14, -0.09, 0.14, 0.09, 0.14, 0.09, -0.14]
- Tile: [6, 1, 1, 4] [0.15, 0.75]
  - Convex: [-0.14, -0.14, -0.14, 0.14, 0.14, 0.14, -0.06, -0.14]
"""

def test_g2s_cleaningGrid():
    # ToDO: add some mechanism to clean a grid map...
    assert True