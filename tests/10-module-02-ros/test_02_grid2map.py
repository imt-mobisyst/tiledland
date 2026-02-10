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
    scene= tll.Scene().fromGridRectangles(grid)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-convexMap-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_smallMap():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asTllGrid()

    scene= tll.Scene().fromGridRectangles( grid )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene.mergeAllPossible( 0.2, 2.0 )

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-small-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_mediumMap_inside():
    gridmap= ros.GridMap().load( "tests/rsc", "medium-map.yaml" )
    grid= gridmap.asTllGrid()
    grid.filter(1, -1)

    #scene= tll.Scene().fromGridRectangles( grid )
    scene= tll.Scene()

    scene.clear()
    scene._epsilon= round( grid.resolution() * 0.4, 4 )
    tileSize= 4.0

    print( f"From grid: {scene._epsilon} {tileSize}" )
    assert scene.epsilon() == 0.04

    # Foreach value possibility:
    minMatter, maxMatter= grid.valueMinMax()
    assert (minMatter, maxMatter) == (0, 0)
    i= 0
    for matter in range( minMatter, maxMatter+1 ):
        # Add all shapes
        shapes= grid.makeRectangles(matter, tileSize)
        for s in shapes :
            i+= 1
            assert scene.createTile(s, matter) == i

    # Connect all elements:
    scene.connectAllClose( grid.resolution() )
    print( f"From grid: {scene._epsilon} {tileSize}" )

    # Optimize the definition:
    for factor in [0.2, 0.4, 0.6, 0.8] :
        scene.mergeAllPossible( grid.resolution()*factor, tileSize)

    ## end fromGrid

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg )
    refsFile= open( "tests/refs/interface-ros-02-medium-01.svg" )
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_mediumMap():
    gridmap= ros.GridMap().load( "tests/rsc", "medium-map.yaml" )
    grid= gridmap.asTllGrid()
    grid.filter(1, -1)

    scene= tll.Scene().fromGridRectangles( grid, 4.0 )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-medium-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

""" 
def test_gridmap_largeMap():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asTllGrid()
    grid.filter(1, -1)

    scene= tll.Scene().fromGridRectangles( grid, 4.0 )
    
    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-02-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
"""
