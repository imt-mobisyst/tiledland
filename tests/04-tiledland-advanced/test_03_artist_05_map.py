import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tll
from src.tiledland.geometry import Point, Convex

def zipSvgFile( img1, img2 ):
    shotFile= open( img1 ) 

    refsFile= open( img2 )
    return zip( shotFile, refsFile )

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #
shotImg= "shot-test.svg"

# Test artist on tiles
def test_artist_tile():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    tile= tll.Tile()
    
    tile.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-01.svg" ):
        assert( lineShot == lineRef )
    
    tile= tll.Tile( 3, 0, Convex().initSquare(4.0) )
    tile.setPosition(1.3, 0.9)
    tile.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-02.svg" ):
        assert( lineShot == lineRef )

    tile= tll.Tile(1, 1).setPosition( Point(0.4, 0.2) )
    tile.shape().initRegular( 2.0, 6 )
    tile.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-03.svg" ):
        assert( lineShot == lineRef )

    tile.renderOn( pablo )
    tile.writeOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-04.svg" ):
        assert( lineShot == lineRef )

# Test artist on map
def test_artist_map_tiles():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    map= tll.Map()

    assert map.epsilon() == 0.01
        
    map.renderTilesOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-00.svg" ):
        assert( lineShot == lineRef )

    map= tll.Map().initLine(3)

    assert map.epsilon() == 0.01

    map.renderTilesOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-01.svg" ):
        assert( lineShot == lineRef )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    map.renderTilesOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-02.svg" ):
        assert( lineShot == lineRef )

def test_artist_map_net():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    map= tll.Map()
    map.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-14.svg" ):
        assert( lineShot == lineRef )

    box= map.box()
    box.round(2)
    assert box.asZip() == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fit( map )
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-15.svg" ):
        assert( lineShot == lineRef )

    map.connectAllConditions(
        lambda tileFrom : tileFrom.matter() == 0,
        lambda tileFrom, tileTo : tileTo.matter() == 0 and tileFrom.centerDistance( tileTo ) < 1.2
    )
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-map-16.svg" ):
        assert( lineShot == lineRef )


# Test artist on map
def test_artist_gridmap_piece():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    map= tll.Map()
    map.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( map.box() )
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-01.svg" ):
        assert( lineShot == lineRef )

    def popAgent( iRobot, iMatter, iTile ):
        bob= tll.Agent( iRobot, 0,
            Point(0.1, 0.1)+map.tile(iTile).position(),
            tll.Convex().initRegular(0.7, 6),
        )
        bob.setMatter(iMatter)
        map.tile(iTile).append( bob )
        return bob
    
    bob= popAgent(1, 13, 12)

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.shape().asZipped() ]
    print( env )
    assert env == [
        (-0.3, -0.18), (-0.3, 0.17), (-0.0, 0.35),
        (0.3, 0.18), (0.3, -0.17), (0.0, -0.35),
    ]

    bob= map.tile(12).agent()

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.body().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.body().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]
    

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-02.svg" ):
        assert( lineShot == lineRef )
    
    popAgent(2, 13, 9)
    popAgent(2, 15, 14)
    popAgent(3, 13, 23)
    popAgent(1, 15, 20)

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-03.svg" ):
        assert( lineShot == lineRef )

    popAgent(1, 1, 17)
    
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-04.svg" ):
        assert( lineShot == lineRef )

    map.clearAgents()
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-01.svg" ):
        assert( lineShot == lineRef )

# Test artist on map
def test_artist_hexamap_piece():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    map= tll.Map()
    map.initHexa(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( map.box() )
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-11.svg" ):
        assert( lineShot == lineRef )

    def popAgent( iRobot, iTile, iMatter ):
        bod= tll.Agent( iRobot, 0,
            Point(0.1, 0.1)+map.tile(iTile).position(),
            tll.Convex().initRegular(0.7, 6),
        )
        bod.setMatter(iMatter)
        map.tile(iTile).append( bod )
    
    popAgent(1, 12, 13)

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-12.svg" ):
        assert( lineShot == lineRef )
    
    popAgent(2,  9, 13)
    popAgent(2, 14, 15)
    popAgent(3, 23, 13)
    popAgent(1, 20, 15)

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-13.svg" ):
        assert( lineShot == lineRef )

    popAgent(1, 17, 1)

    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-14.svg" ):
        assert( lineShot == lineRef )

    map.clearAgents()
    map.renderOn( pablo )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-11.svg" ):
        assert( lineShot == lineRef )
