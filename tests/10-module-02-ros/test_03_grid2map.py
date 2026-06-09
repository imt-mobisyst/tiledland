# HackaGames UnitTest - `pytest`
import sys, re
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex, Grid
from src.tiledland import Agent, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland.interface import ros

def test_long_gridmap_loadSmallMap():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asGrid()

    assert gridmap.resolution() == 0.1

    convexes= grid.makeConvexes(0, 8)
    tll.artist.drawConvexes(convexes)
    assert len(convexes) == 17
    
    scene= tll.Scene().fromGridConvexes( grid, 2.0, matters=[Grid.STATE_FREE] )

    tll.artist.drawScene(scene)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)
    pablo.fit(scene)

    tll.artist.drawScene(scene)

    scene.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene= tll.Scene().fromGridConvexes( grid, 2.0 )

    tll.artist.drawScene(scene)
    
    scene.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-02.svg" )
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_long_gridmap_loadLargeMap():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asGrid()

    assert gridmap.resolution() == 0.1

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)

    scene= tll.Scene().fromGridConvexes( grid, 2.0, matters=[Grid.STATE_FREE] )

    tll.artist.drawScene(scene)

    pablo.fit(scene)
    scene.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene= tll.Scene().fromGridConvexes( grid, 2.0 )
    
    tll.artist.drawScene(scene)
    
    pablo.fit(scene)
    scene.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_rosGridMap_webots():
    gridmap= Grid()

    rosFile= open( r"tests/rsc/webot-map.log", "r" )
    meta= rosFile.readline().strip()
    assert meta == "map: 103x162 at 0.05 on (-1.4355376215141014, -3.1116143188991185)"
    patern= re.compile( r"map: ([\d]+)x([\d]+) at ([\d\.]+) on \((\-?[\d\.]+), (\-?[\d\.]+)\)" )
    selects= list(patern.search(meta).groups())
    assert selects == [ '103', '162', '0.05', '-1.4355376215141014', '-3.1116143188991185']
    
    width= int(selects[0])
    height= int(selects[1])
    resolution= float(selects[2]) 
    pos_x= float(selects[3]) 
    pos_y= float(selects[4])

    assert [width, height, resolution, pos_x, pos_y] == [ 103, 162, 0.05, -1.4355376215141014, -3.1116143188991185]

    grid= [
        [ int(v) for v in line.strip().split(' ') ]
        for line in rosFile
    ]

    rosFile.close

    assert len(grid) == height
    assert len(grid[0]) == width
    assert len(grid[42]) == width
    assert len(grid[161]) == width

    gridmap= ros.transformOccupMap( grid, (pos_x, pos_y), resolution )

    assert gridmap.resolution() == 0.05
    assert gridmap.bottomleft().asTuple() == (-1.4355376215141014, -3.1116143188991185)
    assert gridmap.dimention() == (103, 162)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg, 800, 600)

    scene= tll.Scene().fromGridConvexes( gridmap, 2.0, matters=[Grid.STATE_FREE, Grid.STATE_OCCUPIED] )
    pablo.fit(scene)
    scene.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-webots-map.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

