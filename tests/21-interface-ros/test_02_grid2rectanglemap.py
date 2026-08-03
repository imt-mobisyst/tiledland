# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Agent, Tile, Tabletop 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland.interface import ros

def test_gridmap_asGrid():
    gridmap= ros.GridMap()
    
    gridmap._grid= [
        [1.0, 0.5, 0.0, 0.0],
        [0.0, 0.3, 0.9, 0.0],
        [0.0, 0.0, 0.1, 0.0]
    ]
    assert gridmap.dimention() == (4, 3)

    grid= gridmap.asGrid()
    
    assert type(grid) == tll.Grid
    assert grid.dimention() == (4, 3)
    assert grid.values() == [
        [1, 2, 0, 0],
        [0, 2, 1, 0],
        [0, 0, 0, 0]
    ]

def test_long_gridmap_rectangletabletop():
    gridmap= ros.GridMap().load( "tests/rsc", "convexmap.yaml" )
    grid= gridmap.asGrid()
    tabletop= tll.Tabletop().fromGridRectangles(grid)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(tabletop)

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/21.02-convexMap-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_long_gridmap_smallTabletop():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asGrid()

    tabletop= tll.Tabletop().fromGridRectangles( grid )

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(tabletop)

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/21.02-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    tabletop.mergeAllPossible( 0.2, 2.0 )

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/21.02-small-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_long_gridmap_mediumTabletop_inside():
    gridmap= ros.GridMap().load( "tests/rsc", "medium-map.yaml" )
    grid= gridmap.asGrid()
    grid.filter(1, -1)

    #tabletop= tll.Tabletop().fromGridRectangles( grid )
    tabletop= tll.Tabletop()

    tabletop.clear()
    tabletop._epsilon= round( grid.resolution() * 0.4, 4 )
    tileSize= 4.0

    print( f"From grid: {tabletop._epsilon} {tileSize}" )
    assert tabletop.epsilon() == 0.04

    # Foreach value possibility:
    minVal, maxVal= grid.valueMinMax()
    assert (minVal, maxVal) == (0, 0)
    i= 0
    for pixval in range(minVal, maxVal+1):
        # Add all shapes
        shapes= grid.makeRectangles(pixval, tileSize)
        for s in shapes :
            i+= 1
            assert tabletop.createTile(s, pixval) == i

    # Connect all elements:
    tabletop.connectAllClose( grid.resolution() )
    print( f"From grid: {tabletop._epsilon} {tileSize}" )

    # Optimize the definition:
    for factor in [0.2, 0.4, 0.6, 0.8] :
        tabletop.mergeAllPossible( grid.resolution()*factor, tileSize)

    ## end fromGrid

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(tabletop)

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg )
    refsFile= open( "tests/refs/21.02-medium-01.svg" )
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_long_gridmap_mediumTabletop():
    gridmap= ros.GridMap().load( "tests/rsc", "medium-map.yaml" )
    grid= gridmap.asGrid()
    grid.filter(1, -1)

    tabletop= tll.Tabletop().fromGridRectangles( grid, 4.0 )

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(tabletop)

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/21.02-medium-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

""" 
def test_gridmap_largeTabletop():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asGrid()
    grid.filter(1, -1)

    tabletop= tll.Tabletop().fromGridRectangles( grid, 4.0 )
    
    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(tabletop)

    tll.draw(tabletop)
    tabletop.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/21.02-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
"""
