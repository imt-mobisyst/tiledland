# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Agent, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland import rosi

def test_gridmap_cells():
    gridmap= rosi.GridMapStat()
    
    gridmap.setGrid([
        [1.0, 0.5, 0.0, 0.0],
        [0.0, 0.2, 0.9, 0.0],
        [0.0, 0.0, 0.1, 0.0]
    ])

    assert gridmap.dimention() == (4, 3)
    assert gridmap.cell(0, 0) == 0.0
    assert gridmap.cellIsFree(0, 0) 
    assert not gridmap.cellIsOccupied(0, 0)
    assert not gridmap.cellIsUncertain(0, 0) 

    assert not gridmap.cellIsFree(0, 2) 
    assert gridmap.cellIsOccupied(0, 2)
    assert not gridmap.cellIsUncertain(0, 2) 

    assert not gridmap.cellIsFree(1, 2) 
    assert not gridmap.cellIsOccupied(1, 2)
    assert gridmap.cellIsUncertain(1, 2) 

    assert gridmap.cellIsFree(2, 0)
    assert gridmap.cellIsOccupied(2, 1)

    realGridmap= gridmap.asGridMap()
        
    realGridmap.setGrid([
        [1, 2, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ])

def test_gridmap_boxing():
    gridmap= rosi.GridMap()
    
    gridmap.setGrid([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ])

    assert gridmap.box(0, 0) == [0, 0, 1, 1]

    gridmap.setGrid([
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 1]

    gridmap.setGrid([
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 2]

    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 4, 3]

    gridmap.setGrid([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 3]

    gridmap.setGrid([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 3]

def test_gridmap_search():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert gridmap.search() == (0, 0)
    assert gridmap.search(1) == False

    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [2, 2, 0, 0]
    ])
    assert gridmap.search() == (2, 0)
    assert gridmap.search(1) == (2, 1)

def test_gridmap_allbox():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    boxes= gridmap.makeBoxes()
    assert boxes == [ [0, 0, 4, 3] ]

    print( "Grid" )
    for line in gridmap.grid() :
        print(line)

    assert gridmap.grid() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ])
    boxes= gridmap.makeBoxes()

    print( "Boxes" )
    for box in boxes :
        print(box)

    assert boxes == [
        [0, 0, 2, 3],
        [2, 0, 4, 1],
        [3, 1, 4, 3],
        [2, 2, 3, 3]
    ]

    print( "Grid" )
    for line in gridmap.grid() :
        print(line)

    assert gridmap.grid() == [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]

    gridmap.setGrid([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])
    boxes= gridmap.makeBoxes()

    print( "Boxes" )
    for box in boxes :
        print(box)

    assert boxes == [
        [0, 0, 8, 7],
        [8, 0, 19, 2],
        [21, 0, 24, 7],
        [10, 2, 19, 4],
        [14, 4, 19, 7],
        [8, 5, 14, 7],
        [19, 5, 21, 7]
    ]

def test_gridmap_asRectangles():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    boxes= gridmap.makeBoxes()

    print( "Boxes" )
    for box in boxes :
        print(box)
    
    assert boxes == [
        [0, 0, 10, 7],
        [10, 0, 16, 3],
        [13, 3, 16, 12],
        [0, 7, 5, 12],
        [5, 9, 13, 12]
    ]

    shape= gridmap.boxToShape( [5, 9, 13, 12] )
    
    print( "Shape: " + str(shape) + " - " + str( shape.asZipped() ) )
    
    assert shape.asZipped() == [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)]
    shapes= gridmap.makeShapes()
    shapesAsZipped= [ s.asZipped() for s in shapes ]

    print( "Shapes" )
    for s in shapesAsZipped :
        print(s)

    assert shapesAsZipped == [
        [(0.125, 0.125), (0.125, 3.375), (4.875, 3.375), (4.875, 0.125)],
        [(5.125, 0.125), (5.125, 1.375), (7.875, 1.375), (7.875, 0.125)],
        [(6.625, 1.625), (6.625, 5.875), (7.875, 5.875), (7.875, 1.625)],
        [(0.125, 3.625), (0.125, 5.875), (2.375, 5.875), (2.375, 3.625)],
        [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)]
    ]

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setCamera( 4.0, 3.0 )

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/11.02-svg-flip-00.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    for shape in shapes :
        pablo.drawShape( shape, 0 )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/22.01-toshapes-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
