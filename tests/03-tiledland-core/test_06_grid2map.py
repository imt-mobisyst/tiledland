import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_g2s_makeRectangles_small():
    grid= tild.Grid()
    grid.init([
        [1, 1, 0,  0, 0],
        [1, 1, 0,  0, 0],
        [0, 0, 0,  0, 0],

        [0, 0, 0,  0, 0],
        [0, 0, 0,  0, 0],
        [0, 0, 0,  0, 0]
    ])

    assert grid.resolution() == 0.1 # dm
    assert grid.bottomleft().asTuple() == (0.0, 0.0)
    shapes= grid.makeRectangles(0)

    assert len(shapes) == 2
    
    print( shapes[0].round(2).asZipped() )
    assert shapes[0].round(2).asZipped() == [
        (0.01, 0.01), (0.01, 0.39), (0.49, 0.39), (0.49, 0.01)
    ]

    print( shapes[1].round(2).asZipped() )
    assert shapes[1].round(2).asZipped() == [
        (0.21, 0.41), (0.21, 0.59), (0.49, 0.59), (0.49, 0.41)
    ]

    # Tabletop Construction :
    tabletop= tild.Map( epsilon=0.06 )
    shapes= grid.makeRectangles(0)
    i= 0
    for s in shapes :
        i+= 1
        assert tabletop.createTile(s, 0) == i
        tabletop.tile(i).shape().round(2)
    assert tabletop.size() == i
    assert i == 2

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-small-01.svg" ).read() )

    shapes= grid.makeRectangles(1)
    for s in shapes :
        i+= 1
        assert tabletop.createTile(s, 1) == i
        tabletop.tile(i).shape().round(2)
    assert tabletop.size() == 3

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-small-02.svg" ).read() )

    tabletop.connectAllClose( grid.resolution() )

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-small-03.svg" ).read() )

    # Tabletop Construction, in short:
    tabletop= tild.Map().fromGridRectangles(grid)
    tabletop._epsilon= round( tabletop._epsilon, 6 )

    for t in tabletop.tiles() :
        t.shape().round(2)
    
    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-small-03.svg" ).read() )


def test_g2s_makeRectangles_medium():
    grid= tild.Grid()
    grid.init([
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

    shapes= grid.makeRectangles(0)

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
    
    shapes= grid.makeRectangles(1)

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
    
    # Tabletop from grid:
    tabletop= tild.Map().fromGridRectangles(grid)

    for t in tabletop.tiles() :
        t.shape().round(2)
    
    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-medium.svg" ).read() )


def test_g2s_makeRectangles_medium_limit():
    tabletop= tild.Map()
    grid= tild.Grid()
    grid.init([
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

    shapes= grid.makeRectangles(0, 0.31)

    tabletop.fromShapes(shapes)
    tabletop.connectAllClose( 0.021 )

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    
    assert len(shapes) == 11
    referes= [
        [(0.01, 0.01), (0.01, 0.29), (0.29, 0.29), (0.29, 0.01)],
        [(0.31, 0.01), (0.31, 0.29), (0.59, 0.29), (0.59, 0.01)],
        [(0.61, 0.01), (0.61, 0.29), (0.89, 0.29), (0.89, 0.01)],
        
        [(0.01, 0.31), (0.01, 0.59), (0.29, 0.59), (0.29, 0.31)],
        [(0.31, 0.31), (0.31, 0.59), (0.39, 0.59), (0.39, 0.31)],
        [(0.61, 0.31), (0.61, 0.59), (0.89, 0.59), (0.89, 0.31)],
        
        [(0.11, 0.61), (0.11, 0.69), (0.39, 0.69), (0.39, 0.61)],
        [(0.41, 0.61), (0.41, 0.89), (0.69, 0.89), (0.69, 0.61)],
        [(0.71, 0.61), (0.71, 0.89), (0.89, 0.89), (0.89, 0.61)],
        
        [(0.21, 0.71), (0.21, 0.79), (0.39, 0.79), (0.39, 0.71)],
        [(0.31, 0.81), (0.31, 0.89), (0.39, 0.89), (0.39, 0.81)]
    ]

    print( '-'*10 )
    for shape, ref  in zip( shapes, referes ) :
        print( shape.round(2).asZipped() )
        assert shape.asZipped() ==  ref

    refCat= tabletop.tile(1).category()
    assert tabletop.selectId(lambda t : t.category() == refCat) == [i for i in range(1, 12)]
    assert tabletop.selectIdSmallbox(0.16) == [5, 7, 10, 11]

    assert( tabletop.mergeTile(5, 0.06, 1.0) )
    
    body4= tabletop.tile(4).shape().round(2).asZipped()
    print( body4 )
    assert body4 ==  [(0.01, 0.31), (0.01, 0.59), (0.39, 0.59), (0.39, 0.31)]
    
    assert( tabletop.mergeTile(6, 0.06, 1.0) )
    
    body6= tabletop.tile(6).shape().round(2).asZipped()
    print(body6)
    assert body6 ==  [(0.11, 0.61), (0.11, 0.69), (0.21, 0.79), (0.39, 0.79), (0.39, 0.61)]
    tabletop.mergeAllPossible( 0.06, 0.31 )

    for t in tabletop.tiles() :
        t.shape().round(2)
    
    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.06-grid-makeRectangles-medium-02.svg" ).read() )

def test_makeConvexes_small():
    grid= tild.Grid([
        [0, 0, 0, 0, 1,  1, 1, 1, 1, 1 ],
        [0, 0, 0, 0, 0,  1, 1, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  1, 1, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  1, 1, 0, 0, 0 ],
        [0, 0, 1, 0, 0,  1, 1, 0, 0, 0 ],

        [0, 0, 1, 0, 0,  0, 1, 0, 0, 0 ],
        [0, 0, 1, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 1, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ]
    ], tild.Point(0.5, 0.5), 1.0 )
    print(grid)
    
    tabletop= tild.Map().fromGridConvexes(grid, 1.0, pixelValues=[tild.Grid.STATE_FREE])

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    
    print('\n'+ str(tabletop) +'.')
    assert '\n'+str(tabletop) == """
Map:
- Tile 0-1 ⌊(4.5, 1.5), (9.5, 5.5)⌉ adjs[2, 3, 4] units(0)
- Tile 0-2 ⌊(8.5, 2.5), (10.5, 9.5)⌉ adjs[1] units(0)
- Tile 0-3 ⌊(1.5, 6.5), (5.5, 10.5)⌉ adjs[1, 4] units(0)
- Tile 0-4 ⌊(1.5, 1.5), (3.5, 5.5)⌉ adjs[1, 3] units(0)"""

    tabletop= tild.Map().fromGridConvexes(grid, 1.0)

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )

    print('\n'+ str(tabletop) +'.')
    assert '\n'+str(tabletop) == """
Map:
- Tile 0-1 ⌊(4.5, 1.5), (9.5, 5.5)⌉ adjs[2, 3, 4, 5] units(0)
- Tile 0-2 ⌊(8.5, 2.5), (10.5, 9.5)⌉ adjs[1, 5, 6] units(0)
- Tile 0-3 ⌊(1.5, 6.5), (5.5, 10.5)⌉ adjs[1, 4, 5, 6] units(0)
- Tile 0-4 ⌊(1.5, 1.5), (3.5, 5.5)⌉ adjs[1, 3] units(0)
- Tile 0-5 ⌊(6.5, 5.5), (7.5, 7.5)⌉ adjs[1, 2, 3, 6] units(0)
- Tile 0-6 ⌊(5.5, 8.5), (10.5, 10.5)⌉ adjs[2, 3, 5] units(0)"""

def test_makeConvexes_medium():
    grid= tild.Grid([
        [0, 0, 0, 0, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1 ],
        [0, 0, 0, 0, 0,  1, 1, 0, 0, 0,  1, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1 ],
        [1, 0, 0, 0, 0,  1, 1, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1 ],
        [1, 1, 0, 0, 0,  1, 1, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 1, 1, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 1, 1, 1, 1 ],
        [1, 0, 0, 0, 0,  1, 1, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 1, 1, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 1, 1, 1, 1 ],

        [0, 0, 0, 0, 0,  0, 1, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 1, 1 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 1, 1 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 1, 1, 1, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],

        [1, 0, 0, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 1, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 1, 1, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [1, 1, 1, 1, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [1, 1, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 1, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],

        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1, 0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 1, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 1, 1, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0 ],

        [0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  1, 1, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 1, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  1, 1, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 1,  1, 1, 1, 1, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],

        [0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ],
        [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 1,  1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0 ]
    ], tild.Point(0.5, 0.5), 1.0 )
    print(grid)
    
    tabletop= tild.Map().fromGridConvexes(grid, 8.0, 0.01, pixelValues=[tild.Grid.STATE_FREE])
    tild.drawMap( tabletop, "shot-test.png", 800, 600 )

    print('\n'+ str(tabletop) +'.')
    assert '\n'+str(tabletop) == """
Map:
- Tile 0-1 ⌊(1.5, 1.5), (9.5, 10.5)⌉ adjs[2, 5] units(0)
- Tile 0-2 ⌊(10.5, 1.5), (19.5, 11.5)⌉ adjs[1, 5, 6] units(0)
- Tile 0-3 ⌊(21.5, 1.5), (28.5, 10.5)⌉ adjs[4, 6] units(0)
- Tile 0-4 ⌊(29.5, 1.5), (35.5, 10.5)⌉ adjs[3, 7] units(0)
- Tile 0-5 ⌊(1.5, 10.5), (13.5, 16.5)⌉ adjs[1, 2, 6, 8, 9] units(0)
- Tile 0-6 ⌊(14.5, 9.5), (25.5, 18.5)⌉ adjs[2, 3, 5, 9] units(0)
- Tile 0-7 ⌊(27.5, 10.5), (35.5, 17.5)⌉ adjs[4, 10, 11] units(0)
- Tile 0-8 ⌊(1.5, 15.5), (10.5, 22.5)⌉ adjs[5, 9, 12, 15] units(0)
- Tile 0-9 ⌊(11.5, 14.5), (19.5, 24.5)⌉ adjs[5, 6, 8, 12, 13] units(0)
- Tile 0-10 ⌊(24.5, 17.5), (29.5, 24.5)⌉ adjs[7, 11, 13, 14] units(0)
- Tile 0-11 ⌊(30.5, 18.5), (35.5, 25.5)⌉ adjs[7, 10, 14] units(0)
- Tile 0-12 ⌊(8.5, 22.5), (16.5, 29.5)⌉ adjs[8, 9, 13, 15] units(0)
- Tile 0-13 ⌊(17.5, 21.5), (24.5, 30.5)⌉ adjs[9, 10, 12, 14] units(0)
- Tile 0-14 ⌊(23.5, 25.5), (31.5, 30.5)⌉ adjs[10, 11, 13] units(0)
- Tile 0-15 ⌊(1.5, 20.5), (7.5, 30.5)⌉ adjs[8, 12] units(0)"""

    
    tabletop= tild.Map().fromGridConvexes(grid, 8.0)
    tild.drawMap( tabletop, "shot-test.png", 800, 600 )

    print('\n'+ str(tabletop) +'.')
    assert '\n'+str(tabletop) == """
Map:
- Tile 0-1 ⌊(1.5, 1.5), (9.5, 10.5)⌉ adjs[2, 5, 16] units(0)
- Tile 0-2 ⌊(10.5, 1.5), (19.5, 11.5)⌉ adjs[1, 5, 6, 16, 17, 18] units(0)
- Tile 0-3 ⌊(21.5, 1.5), (28.5, 10.5)⌉ adjs[4, 6, 17, 19] units(0)
- Tile 0-4 ⌊(29.5, 1.5), (35.5, 10.5)⌉ adjs[3, 7, 19] units(0)
- Tile 0-5 ⌊(1.5, 10.5), (13.5, 16.5)⌉ adjs[1, 2, 6, 8, 9, 16, 18] units(0)
- Tile 0-6 ⌊(14.5, 9.5), (25.5, 18.5)⌉ adjs[2, 3, 5, 9, 17, 19, 21, 22] units(0)
- Tile 0-7 ⌊(27.5, 10.5), (35.5, 17.5)⌉ adjs[4, 10, 11, 19] units(0)
- Tile 0-8 ⌊(1.5, 15.5), (10.5, 22.5)⌉ adjs[5, 9, 12, 15, 20] units(0)
- Tile 0-9 ⌊(11.5, 14.5), (19.5, 24.5)⌉ adjs[5, 6, 8, 12, 13, 21] units(0)
- Tile 0-10 ⌊(24.5, 17.5), (29.5, 24.5)⌉ adjs[7, 11, 13, 14, 22] units(0)
- Tile 0-11 ⌊(30.5, 18.5), (35.5, 25.5)⌉ adjs[7, 10, 14, 25] units(0)
- Tile 0-12 ⌊(8.5, 22.5), (16.5, 29.5)⌉ adjs[8, 9, 13, 15, 23, 24] units(0)
- Tile 0-13 ⌊(17.5, 21.5), (24.5, 30.5)⌉ adjs[9, 10, 12, 14, 21, 22, 24] units(0)
- Tile 0-14 ⌊(23.5, 25.5), (31.5, 30.5)⌉ adjs[10, 11, 13, 25] units(0)
- Tile 0-15 ⌊(1.5, 20.5), (7.5, 30.5)⌉ adjs[8, 12, 20, 23, 26] units(0)
- Tile 0-16 ⌊(5.5, 5.5), (10.5, 10.5)⌉ adjs[1, 2, 5, 18] units(0)
- Tile 0-17 ⌊(20.5, 1.5), (21.5, 9.5)⌉ adjs[2, 3, 6] units(0)
- Tile 0-18 ⌊(7.5, 8.5), (12.5, 12.5)⌉ adjs[2, 5, 16] units(0)
- Tile 0-19 ⌊(25.5, 9.5), (30.5, 16.5)⌉ adjs[3, 4, 6, 7, 22] units(0)
- Tile 0-20 ⌊(1.5, 17.5), (6.5, 21.5)⌉ adjs[8, 15] units(0)
- Tile 0-21 ⌊(16.5, 19.5), (20.5, 21.5)⌉ adjs[6, 9, 13, 22] units(0)
- Tile 0-22 ⌊(21.5, 16.5), (26.5, 22.5)⌉ adjs[6, 10, 13, 19, 21] units(0)
- Tile 0-23 ⌊(5.5, 25.5), (13.5, 30.5)⌉ adjs[12, 15, 24] units(0)
- Tile 0-24 ⌊(14.5, 26.5), (20.5, 30.5)⌉ adjs[12, 13, 23] units(0)
- Tile 0-25 ⌊(30.5, 23.5), (35.5, 30.5)⌉ adjs[11, 14] units(0)
- Tile 0-26 ⌊(1.5, 26.5), (2.5, 28.5)⌉ adjs[15] units(0)"""

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
          == open("tests/refs/03.06-grid-makeConvexe-medium.svg" ).read() )
