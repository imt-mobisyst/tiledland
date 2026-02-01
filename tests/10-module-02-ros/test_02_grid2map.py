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

def test_gridmap_asGrid():
    gridmap= ros.GridMap()
    
    gridmap._grid= [
        [1.0, 0.5, 0.0, 0.0],
        [0.0, 0.3, 0.9, 0.0],
        [0.0, 0.0, 0.1, 0.0]
    ]
    assert gridmap.dimention() == (4, 3)

    grid= gridmap.asTllGrid()
    
    assert type(grid) == tll.Grid
    assert grid.dimention() == (4, 3)
    assert grid.values() == [
        [1, 2, 0, 0],
        [0, 2, 1, 0],
        [0, 0, 0, 0]
    ]

def test_gridmap_convexMap():
    gridmap= ros.GridMap().load( "tests/rsc", "convexmap.yaml" )
    grid= gridmap.asTllGrid()
    scene= tll.Scene().fromGrid( grid )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.fit(scene)

    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-convexMap-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_smallMap():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asTllGrid()

    scene= tll.Scene().fromGrid( grid )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.fit(scene)

    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_mediumMap():
    gridmap= ros.GridMap().load( "tests/rsc", "medium-map.yaml" )
    grid= gridmap.asTllGrid()

    scene= tll.Scene().fromGrid( grid )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.fit(scene)

    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-medium-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_largeMap():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asTllGrid()
    scene= tll.Scene().fromGrid( grid )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.fit(scene)

    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    

