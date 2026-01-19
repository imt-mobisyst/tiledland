import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tll
from src.tiledland.geometry import Point, Shape

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
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    tile= tll.Tile()
    
    pablo.drawTile( tile )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-01.svg" ):
        assert( lineShot == lineRef )
    
    tile= tll.Tile( 3, Point(1.3, 0.9), Shape().initializeSquare(4.0) )
    pablo.drawTile( tile )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-02.svg" ):
        assert( lineShot == lineRef )

    tile= tll.Tile( 1, matter=1 ).setPosition( Point(0.4, 0.2) )
    tile.shape().initializeRegular( 2.0, 6 )
    pablo.drawTile( tile )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-03.svg" ):
        assert( lineShot == lineRef )

    pablo.drawTile( tile )
    pablo.writeTile( tile )
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-tile-04.svg" ):
        assert( lineShot == lineRef )

# Test artist on scene
def test_artist_scene_tiles():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()

    assert scene.resolution() == 0.01
        
    pablo.drawSceneTiles(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-00.svg" ):
        assert( lineShot == lineRef )

    scene= tll.Scene().initializeLine(3)

    assert scene.resolution() == 0.1

    pablo.drawSceneTiles(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-01.svg" ):
        assert( lineShot == lineRef )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    pablo.drawSceneTiles(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-02.svg" ):
        assert( lineShot == lineRef )


def test_artist_scene_net():
    pablo= tll.Artist( tll.SupportSVG( filePath= shotImg ) )
    scene= tll.Scene()
    
    assert scene.addTile( tll.Tile().setShapeRegular( (-1.0, 0.0), 0.9, 6 ) ) == 1
    assert scene.addTile( tll.Tile( matter=1 ).setShapeRegular( (0.0, 0.0), 0.9, 6 ) ) == 2
    assert scene.addTile( tll.Tile().setShapeRegular( (1.0, 0.0), 0.9, 6 ) ) == 3

    assert scene.addTile( tll.Tile().setShapeRegular( (0.5, 0.866), 0.9, 6 ) ) == 4
    assert scene.addTile( tll.Tile().setShapeRegular( (-0.5, -0.866), 0.9, 6 ) ) == 5

    pablo.drawSceneTiles(scene)
    pablo.writeSceneTiles(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-11.svg" ):
        assert( lineShot == lineRef )

    scene.connectAll( [ [1, 2], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4] ] )

    pablo.drawSceneNetwork(scene)
    pablo.writeSceneTiles(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-12.svg" ):
        assert( lineShot == lineRef )

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-13.svg" ):
        assert( lineShot == lineRef )

def test_artist_scene_net():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    scene.initializeGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-14.svg" ):
        assert( lineShot == lineRef )

    box= scene.box()
    box.round(2)
    assert box.asZip() == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fitBox( scene.box() )
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-15.svg" ):
        assert( lineShot == lineRef )

    scene.connectAllConditions(
        lambda tileFrom : tileFrom.matter() == 0,
        lambda tileFrom, tileTo : tileTo.matter() == 0 and tileFrom.centerDistance( tileTo ) < 1.2
    )
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-scene-16.svg" ):
        assert( lineShot == lineRef )


# Test artist on scene
def test_artist_gridscene_piece():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    scene.initializeGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1, False
    )
    scene.connectAllClose()

    pablo.fitBox( scene.box() )
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-01.svg" ):
        assert( lineShot == lineRef )

    def popAgent( iRobot, iTile, iMatter ):
        bod= tll.Agent( iRobot, 0,
            Point(0.1, 0.1)+scene.tile(iTile).position(),
            tll.Shape().initializeRegular(0.7, 6),
        )
        bod.setMatter(iMatter)
        scene.tile(iTile).append( bod )
    
    popAgent(1, 12, 13)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-02.svg" ):
        assert( lineShot == lineRef )
    
    popAgent(2,  9, 13)
    popAgent(2, 14, 15)
    popAgent(3, 23, 13)
    popAgent(1, 20, 15)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-03.svg" ):
        assert( lineShot == lineRef )

    popAgent(1, 17, 1)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-04.svg" ):
        assert( lineShot == lineRef )

    scene.clearAgents()
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-01.svg" ):
        assert( lineShot == lineRef )

# Test artist on scene
def test_artist_hexascene_piece():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    scene.initializeHexa(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1, False
    )
    scene.connectAllClose()

    pablo.fitBox( scene.box() )
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-11.svg" ):
        assert( lineShot == lineRef )

    def popAgent( iRobot, iTile, iMatter ):
        bod= tll.Agent( iRobot, 0,
            Point(0.1, 0.1)+scene.tile(iTile).position(),
            tll.Shape().initializeRegular(0.7, 6),
        )
        bod.setMatter(iMatter)
        scene.tile(iTile).append( bod )
    
    popAgent(1, 12, 13)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-12.svg" ):
        assert( lineShot == lineRef )
    
    popAgent(2,  9, 13)
    popAgent(2, 14, 15)
    popAgent(3, 23, 13)
    popAgent(1, 20, 15)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-13.svg" ):
        assert( lineShot == lineRef )

    popAgent(1, 17, 1)

    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-14.svg" ):
        assert( lineShot == lineRef )

    scene.clearAgents()
    pablo.drawScene(scene)
    pablo.flip()

    for lineShot, lineRef in zipSvgFile( shotImg, "tests/refs/11.11-artist-agent-11.svg" ):
        assert( lineShot == lineRef )
