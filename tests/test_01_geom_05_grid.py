# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Grid

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_grid_init():
    grid= Grid()

    assert type(grid) == Grid
    assert grid.height() == 1
    assert grid.width() == 1
    assert grid.dimention() == (1, 1)
    assert grid.values() == [[0]]
    
    assert grid.position().asTuple() == (0.0, 0.0)
    assert grid.resolution() == 0.1

def test_grid_init2():
    grid= Grid( [
        [0, 0, 1],
        [1, 0, 2]
    ])

    assert type(grid) == Grid
    assert grid.height() == 2
    assert grid.width() == 3
    assert grid.dimention() == (3, 2)
    assert grid.position().asTuple() == (0.0, 0.0)
    assert grid.resolution() == 0.1

    assert grid.values() == [
        [0, 0, 1],
        [1, 0, 2]
    ]

    assert grid.inTable(1, 1) == (1, 0)
    assert grid.cell(1, 1) == 1
    assert grid.cell(2, 1) == 0
    assert grid.cell(3, 1) == 2
    assert grid.cell(2, 2) == 0
    assert grid.cell(3, 2) == 1

    assert grid.valueMinMax() == (0, 2)

    grid.setCell(1, 2, 4)

    assert grid.values() == [
        [4, 0, 1],
        [1, 0, 2]
    ]
    assert grid.cell(1, 2) == 4

def test_grid_boxing():
    grid= Grid()
    
    grid.initialize([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ])

    assert grid.maxRectangle(1, 1, 10) == [1, 1, 1, 1]

    grid.initialize([
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0]
    ])
    assert grid.maxRectangle(1, 1, 10) == [1, 1, 2, 1]

    grid.initialize([
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert grid.maxRectangle(1, 1, 10) == [1, 1, 2, 2]

    grid.initialize([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert grid.maxRectangle(1, 1, 10) == [1, 1, 4, 3]

    grid.initialize([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert grid.maxRectangle(1, 1, 10) == [1, 1, 2, 3]

    grid.initialize([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert grid.maxRectangle(1, 1, 10) == [1, 1, 2, 3]

def test_grid_search():
    grid= Grid()
    grid.initialize([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert grid.searchLine() == (1, 1)
    assert grid.searchLine(1) == False

    grid.initialize([
        [0, 0, 0, 3],
        [0, 0, 1, 0],
        [2, 2, 0, 0]
    ])
    assert grid.searchLine() == (3, 1)
    assert grid.searchLine(1) == (3, 2)
    assert grid.searchLine(3) == (4, 3)

def test_grid_allrectangle():
    grid= Grid()
    grid.initialize([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])

    cluster= grid.cutingRectangles(0, 100)
    assert cluster == [ [1, 1, 4, 3] ]

    print( "Grid" )
    for line in grid.values() :
        print(line)

    assert grid.values() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    grid.initialize([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ])

    cluster= grid.cutingRectangles(0, 10)

    print( "Cluster" )
    for rect in cluster :
        print(rect)

    assert cluster == [
        [1, 1, 2, 3],
        [3, 1, 4, 1],
        [4, 2, 4, 3],
        [3, 3, 3, 3]
    ]

    print( "Grid" )
    for line in grid.values() :
        print(line)

    assert grid.values() == [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]

    grid.initialize([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    cluster= grid.cutingRectangles(0, 10)

    print( "Cluster" )
    for rect in cluster :
        print(rect)

    assert cluster == [
        [ 1, 1, 8, 7],
        [ 9, 1, 19, 2],
        [22, 1, 24, 7],
        [11, 3, 19, 4],
        [15, 5, 19, 7],
        [ 9, 6, 14, 7],
        [20, 6, 21, 7]
    ]


def test_grid_str():
    grid= Grid()
    grid.initialize([
        [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 2, 0, 0, 0, 0, 1, 1],
        [0, 0, 2, 2, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0]
    ])

    print(grid)
    assert "\n"+ str(grid) +"\n" == """
Grid 10x7
| 3 3 3 · · · · · · ·
| 3 3 3 · · · · · · ·
| 3 3 · · · · · · 1 1
| · · · 2 · · · · 1 1
| · · 2 2 · · · · 1 1
| · · · · · · · · · ·
| 1 1 · · · 1 1 · · ·
0 -------------------
"""
