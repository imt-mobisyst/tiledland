# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Shape

# ------------------------------------------------------------------------ #
#         T E S T   S C E N E   B U I L D
# ------------------------------------------------------------------------ #

def test_scene_build():
    shapes= [
        Shape().fromZipped( [(0.125, 0.125), (0.125, 3.375), (4.875, 3.375), (4.875, 0.125)]),
        Shape().fromZipped( [(5.125, 0.125), (5.125, 1.375), (7.875, 1.375), (7.875, 0.125)]),
        Shape().fromZipped( [(6.625, 1.625), (6.625, 5.875), (7.875, 5.875), (7.875, 1.625)]),
        Shape().fromZipped( [(0.125, 3.625), (0.125, 5.875), (2.375, 5.875), (2.375, 3.625)]),
        Shape().fromZipped( [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)])
    ]

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setCamera( 4.0, 3.0 )

    for shape in shapes :
        pablo.drawShape( shape, 0 )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/22.01-toshapes-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene= tll.Scene( resolution=0.5 )
    assert scene.resolution() == 0.5
    assert scene.size() == 0

    scene.createTile( shapes[0] )
    assert scene.size() == 1

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12-scene-build-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    
    for s in shapes[1:] :
        scene.createTile( s )
    assert scene.size() == 5

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12-scene-build-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    scene.connectAllClose()

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12-scene-build-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    