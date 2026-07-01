# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Line, Convex
from src.tiledland.artist import palette

# ------------------------------------------------------------------------ #
#         T E S T   S C E N E   B U I L D
# ------------------------------------------------------------------------ #

def test_map_fromConvex():
    shapes= [
        Convex().fromZipped( [(0.125, 0.125), (0.125, 3.375), (4.875, 3.375), (4.875, 0.125)]),
        Convex().fromZipped( [(5.125, 0.125), (5.125, 1.375), (7.875, 1.375), (7.875, 0.125)]),
        Convex().fromZipped( [(6.625, 1.625), (6.625, 5.875), (7.875, 5.875), (7.875, 1.625)]),
        Convex().fromZipped( [(0.125, 3.625), (0.125, 5.875), (2.375, 5.875), (2.375, 3.625)]),
        Convex().fromZipped( [(2.625, 4.625), (2.625, 5.875), (6.375, 5.875), (6.375, 4.625)])
    ]

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setCamera( 4.0, 3.0 )

    for shape in shapes :
        pablo.drawConvex( shape, palette.background[0] )
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-toshapes-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    map= tll.Map( epsilon=0.1 )
    assert map.epsilon() == 0.1
    assert map.size() == 0

    map.createTile( shapes[0] )
    assert map.size() == 1

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-map-build-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    
    for s in shapes[1:] :
        map.createTile( s )
    assert map.size() == 5

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-map-build-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    map.connectAllClose(0.5)

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-map-build-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_map_mergeOne():
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
    
    ## Create the map : 
    map= tll.Map( shapes, 0.09 )
    assert map.size() == 2

    map.connectAllClose(0.16)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-one-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
    
    ## Merge :
    ok= map.mergeTilesIfPossible(1, 2, 0.09, 10.0)

    assert ok

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-one-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_map_mergeNoOne():
    shapes= [
        Convex().fromZipped( [(0.05, 0.05), (0.05, 2.55), (4.95, 2.55), (4.95, 0.05)] ),
        Convex().fromZipped( [(1.75, 2.65), (1.75, 4.75), (4.95, 4.75), (4.95, 2.65)] )
    ]

    ## Create the map : 
    map= tll.Map( shapes )
    map.connectAllClose( 0.16 )

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-noone-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge :
    ok= map.mergeTilesIfPossible(1, 2, 0.09, 10.0)

    assert not ok

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-noone-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    # Encore ...
    shapes= [
        Convex().fromZipped( [(5.05, 0.25), (5.05, 4.35), (5.15, 4.35), (5.15, 0.25)] ),
        Convex().fromZipped( [(1.85, 4.25), (1.85, 4.35), (4.95, 4.35), (4.95, 4.25)] )
    ]

    map= tll.Map( shapes, 0.09 )
    map.connectAllClose(0.11)
    ## Merge :
    assert not map.mergeTilesIfPossible(1, 2, 0.09, 10.0)

def test_map_mergeFew():
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

    map= tll.Map( epsilon=0.0999 )
    for s in shapes :
        map.createTile( s )
    
    map.connectAllClose(0.11)

    assert map.size() == 10

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-few-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge 1-2 :
    ok= map.mergeTilesIfPossible(1, 2, 0.09, 10.0)

    assert ok
    assert len( map.tiles() ) == 9
    assert map.size() == 9

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-few-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge 8-9 :
    assert map.mergeTilesIfPossible(8, 9, 0.09, 10.0)

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-few-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    map.mergeAllPossible(0.09, 10.0)
    tll.draw(map)

    map.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-few-04.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_map_mergeConplex():
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

    map= tll.Map( epsilon=0.0999 )
    for s in shapes :
        map.createTile( s )
    
    map.connectAllClose(0.11)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-complex-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    nbMerges= map.mergeAllPossible()

    tll.draw(map)
    assert nbMerges == 12

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-complex-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_map_mergeButNo():
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

    map= tll.Map( epsilon=0.0999 )
    for s in shapes :
        map.createTile( s )
    
    map.connectAllClose(0.11)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.setScale( 100 )
    pablo.setCamera( 3.0, 2.0 )

    map.renderOn(pablo)
    pablo.flip()
    
    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-complex2-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    ## Merge all :
    map.mergeAllPossible()

    map.renderOn(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/04.03-mergeConvex-complex2-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
