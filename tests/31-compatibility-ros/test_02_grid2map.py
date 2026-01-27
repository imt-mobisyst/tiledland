# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Agent, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland.interface import ros

def test_gridmap_cells():
    gridmap= ros.GridMapStat()
    
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

def test_gridmap_asRectangles():
    gridmap= ros.GridMap()
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

    shape= gridmap.boxToConvex( [5, 9, 13, 12] )
    
    print( "Convex: " + str(shape) + " - " + str( shape.asZipped() ) )
    
    assert shape.asZipped() == [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)]
    shapes= gridmap.makeConvexs()
    shapesAsZipped= [ s.asZipped() for s in shapes ]

    print( "Convexs" )
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
        pablo.drawConvex( shape, 0 )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/22.01-toshapes-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )


def test_gridmap_convex():
    shotImg= "shot-test.svg"
    gridmap= ros.GridMapStat()
    pablo= tll.Artist().initializeSVG(shotImg)

    gridmap.load( "tests/rsc", "convexmap.yaml" )
    gridmap= gridmap.asGridMap()

    shapes= gridmap.makeConvexs()

    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )
    for shape in shapes :
        pablo.drawConvex( shape, 0 )
        print( shape.asZipped() )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/22.02-convex2map-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    
    assert False

def test_gridmap_large():
    shotImg= "shot-test.svg"
    gridmap= ros.GridMapStat()
    pablo= tll.Artist().initializeSVG(shotImg)

    gridmap.load( "tests/rsc", "large-clean-map.yaml" )
    gridmap= gridmap.asGridMap()

    shapes= gridmap.makeConvexs()

    pablo.setScale( 28 )
    pablo.setCamera( 16.5, 13.0 )
    for shape in shapes :
        pablo.drawConvex( shape, 0 )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/22.02-grid2Map-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    

