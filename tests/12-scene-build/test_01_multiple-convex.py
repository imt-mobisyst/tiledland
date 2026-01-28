# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Line, Convex

# ------------------------------------------------------------------------ #
#         T E S T   S C E N E   B U I L D
# ------------------------------------------------------------------------ #

def test_scene_fromConvex():
    shapes= [
        Convex().fromZipped( [(0.125, 0.125), (0.125, 3.375), (4.875, 3.375), (4.875, 0.125)]),
        Convex().fromZipped( [(5.125, 0.125), (5.125, 1.375), (7.875, 1.375), (7.875, 0.125)]),
        Convex().fromZipped( [(6.625, 1.625), (6.625, 5.875), (7.875, 5.875), (7.875, 1.625)]),
        Convex().fromZipped( [(0.125, 3.625), (0.125, 5.875), (2.375, 5.875), (2.375, 3.625)]),
        Convex().fromZipped( [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)])
    ]

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setCamera( 4.0, 3.0 )

    for shape in shapes :
        pablo.drawConvex( shape, 0 )
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

    scene.connectAllClose(0.5)

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12-scene-build-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_scene_mergeOne():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(0.25, 2.65), (0.25, 2.75), (4.95, 2.75), (4.95, 2.65)] )
    ]

    ## verify that the 2 shapes should be merged : 
    shape= shapes[0].copy()
    shapeTmp= shapes[1].copy()

    assert shape.distance( shapeTmp ) < 0.2
    trace= [ str(s) for s in shape._trace ]
    print( trace )
    assert trace == ['(0.05, 2.55)->(4.95, 2.55)', '(4.95, 2.65)->(0.25, 2.65)']
    
    print( shape.asZipped() )
    assert shape.asZipped() == [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)]

    removed= shape.merge( shapeTmp )
    assert [(p.x(), p.y()) for p in removed ] == [(0.25, 2.65)]

    for p in removed :
        assert shape.distancePoint(p) < 0.09
    
    ## Create the scene : 
    scene= tll.Scene( shapes, 0.09 )
    assert scene.size() == 2

    scene.connectAllClose(0.16)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-one-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    
    ## Merge :
    ok= scene.mergeTilesIfPossible(1, 2)

    assert ok

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-one-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_scene_mergeNoOne():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(1.75, 2.65), (1.75, 4.75), (4.95, 4.75), (4.95, 2.65)] )
    ]

    ## Create the scene : 
    scene= tll.Scene( shapes )
    scene.connectAllClose( 0.16 )

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-noone-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge :
    ok= scene.mergeTilesIfPossible(1, 2)

    assert not ok

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-noone-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    # Encore ...
    shapes= [
        Convex().fromZipped( [(5.05, 0.25), (5.05, 4.35), (5.15, 4.35), (5.15, 0.25)] ),
        Convex().fromZipped( [(1.85, 4.25), (1.85, 4.35), (4.95, 4.35), (4.95, 4.25)] )
    ]

    scene= tll.Scene( shapes, 0.09 )
    scene.connectAllClose(0.11)
    ## Merge :
    assert not scene.mergeTilesIfPossible(1, 2)

def test_scene_mergeFew():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(0.25, 2.65), (0.25, 2.75), (4.95, 2.75), (4.95, 2.65)] ),
        Convex().fromZipped( [(0.45, 2.85), (0.45, 2.95), (4.95, 2.95), (4.95, 2.85)] ),
        
        Convex().fromZipped( [(0.65, 3.05), (0.65, 3.15), (4.95, 3.15), (4.95, 3.05)] ),
        Convex().fromZipped( [(0.85, 3.25), (0.85, 3.35), (4.95, 3.35), (4.95, 3.25)] ),
        Convex().fromZipped( [(1.05, 3.45), (1.05, 3.55), (4.95, 3.55), (4.95, 3.45)] ),
        
        Convex().fromZipped( [(1.25, 3.65), (1.25, 3.75), (4.95, 3.75), (4.95, 3.65)] ),
        Convex().fromZipped( [(1.45, 3.85), (1.45, 3.95), (4.95, 3.95), (4.95, 3.85)] ),
        Convex().fromZipped( [(1.65, 4.05), (1.65, 4.15), (4.95, 4.15), (4.95, 4.05)] ),
        
        Convex().fromZipped( [(1.85, 4.25), (1.85, 4.35), (4.95, 4.35), (4.95, 4.25)] )
    ]

    scene= tll.Scene( resolution=0.0999 )
    for s in shapes :
        scene.createTile( s )
    
    scene.connectAllClose(0.11)

    assert scene.size() == 10

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-few-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge 1-2 :
    ok= scene.mergeTilesIfPossible(1, 2)

    assert ok
    assert len( scene.tiles() ) == 9
    assert scene.size() == 9

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-few-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge 8-9 :
    assert scene.mergeTilesIfPossible(8, 9)

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-few-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    assert scene.mergeAllPossible() == 7

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-few-04.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_scene_mergeConplex():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(5.05, 0.25), (5.05, 4.35), (5.15, 4.35), (5.15, 0.25)] ),
        Convex().fromZipped( [(5.25, 0.45), (5.25, 4.35), (5.35, 4.35), (5.35, 0.45)] ),
        
        Convex().fromZipped( [(5.45, 0.65), (5.45, 4.35), (5.55, 4.35), (5.55, 0.65)] ),
        Convex().fromZipped( [(0.25, 2.65), (0.25, 2.75), (4.95, 2.75), (4.95, 2.65)] ),
        Convex().fromZipped( [(0.45, 2.85), (0.45, 2.95), (4.95, 2.95), (4.95, 2.85)] ),
        
        Convex().fromZipped( [(0.65, 3.05), (0.65, 3.15), (4.95, 3.15), (4.95, 3.05)] ),
        Convex().fromZipped( [(0.85, 3.25), (0.85, 3.35), (4.95, 3.35), (4.95, 3.25)] ),
        Convex().fromZipped( [(1.05, 3.45), (1.05, 3.55), (4.95, 3.55), (4.95, 3.45)] ),
        
        Convex().fromZipped( [(1.25, 3.65), (1.25, 3.75), (4.95, 3.75), (4.95, 3.65)] ),
        Convex().fromZipped( [(1.45, 3.85), (1.45, 3.95), (4.95, 3.95), (4.95, 3.85)] ),
        Convex().fromZipped( [(1.65, 4.05), (1.65, 4.15), (4.95, 4.15), (4.95, 4.05)] ),
        
        Convex().fromZipped( [(1.85, 4.25), (1.85, 4.35), (4.95, 4.35), (4.95, 4.25)] )
    ]

    scene= tll.Scene( resolution=0.0999 )
    for s in shapes :
        scene.createTile( s )
    
    scene.connectAllClose(0.11)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-complex-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    assert scene.mergeAllPossible() == 12

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-complex-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_scene_mergeButNo():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(0.25, 2.65), (0.25, 2.75), (4.95, 2.75), (4.95, 2.65)] ),
        Convex().fromZipped( [(0.45, 2.85), (0.45, 2.95), (4.95, 2.95), (4.95, 2.85)] ),
        
        Convex().fromZipped( [(0.65, 3.05), (0.65, 3.15), (4.95, 3.15), (4.95, 3.05)] ),
        Convex().fromZipped( [(0.85, 3.25), (0.85, 3.35), (4.95, 3.35), (4.95, 3.25)] ),
        Convex().fromZipped( [(1.05, 3.45), (1.05, 3.55), (4.95, 3.55), (4.95, 3.45)] ),
        
        Convex().fromZipped( [(1.25, 3.65), (1.25, 3.75), (4.95, 3.75), (4.95, 3.65)] ),
        Convex().fromZipped( [(1.45, 3.85), (1.45, 3.95), (4.95, 3.95), (4.95, 3.85)] ),
        Convex().fromZipped( [(1.65, 4.05), (1.65, 4.15), (4.95, 4.15), (4.95, 4.05)] ),
        
        Convex().fromZipped( [(1.85, 4.25), (1.85, 4.35), (4.95, 4.35), (4.95, 4.25)] ),
        Convex().fromZipped( [(5.05, 0.25), (5.05, 3.35), (5.15, 3.35), (5.15, 0.25)] ),
        Convex().fromZipped( [(5.25, 0.45), (5.25, 3.35), (5.35, 3.35), (5.35, 0.45)] ),
        
        Convex().fromZipped( [(5.45, 0.65), (5.45, 3.35), (5.55, 3.35), (5.55, 0.65)] )
    ]

    scene= tll.Scene( resolution=0.0999 )
    for s in shapes :
        scene.createTile( s )
    
    scene.connectAllClose(0.11)

    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG(shotImg)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    pablo.drawScene(scene)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-complex2-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    scene.mergeAllPossible()


    pablo.drawScene(scene)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/12.01-mergeConvex-complex2-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
