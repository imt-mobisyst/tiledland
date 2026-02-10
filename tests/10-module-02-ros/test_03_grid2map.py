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

def test_gridmap_smallMap():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asTllGrid()

    assert gridmap.resolution() == 0.1

    convexes= grid.makeConvexes(0, 8)
    tll.artist.drawConvexes(convexes)
    assert len(convexes) == 17
    
    scene= tll.Scene().fromGridConvexes( grid, 2.0, [0] )

    tll.artist.drawScene(scene)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)

    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene= tll.Scene().fromGridConvexes( grid, 2.0 )

    tll.artist.drawScene(scene)
    
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_largeMap():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asTllGrid()

    assert gridmap.resolution() == 0.1

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)

    scene= tll.Scene().fromGridConvexes( grid, 2.0, [0] )

    tll.artist.drawScene(scene)

    pablo.fit(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene= tll.Scene().fromGridConvexes( grid, 2.0 )
    
    tll.artist.drawScene(scene)
    
    pablo.fit(scene)
    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
