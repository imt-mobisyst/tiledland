import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import hacka.py as hacka
import src.tiledland as tll

def compareSvg( img1, img2 ):
    shotFile= open( img1 ) 
    refsFile= open( img2 ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

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

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-01.svg" )

    tile= tll.Tile( 3, 0, tll.Float2(1.3, 0.9), 4.0 )
    pablo.drawTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-02.svg" )

    tile= tll.Tile( 1, 1 ).setCenter( 0.4, 0.2 ).setShapeRegular( 2.0, 6 )
    pablo.drawTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-03.svg" )

    pablo.drawTile( tile )
    pablo.writeTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-04.svg" )

# Test artist on scene
def test_artist_scene_tiles():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    
    pablo.drawSceneTiles(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-00.svg" )
    
    scene= tll.Scene().initializeLine(3)

    pablo.drawSceneTiles(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-01.svg" )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    pablo.drawSceneTiles(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-02.svg" )

def test_artist_scene_net():
    pablo= tll.Artist( tll.SupportSVG( filePath= shotImg ) )
    scene= tll.Scene()
    
    assert scene.addTile( tll.Tile().setShapeRegular( (-1.0, 0.0), 0.9, 6 ) ) == 1
    assert scene.addTile( tll.Tile( type=1 ).setShapeRegular( (0.0, 0.0), 0.9, 6 ) ) == 2
    assert scene.addTile( tll.Tile().setShapeRegular( (1.0, 0.0), 0.9, 6 ) ) == 3

    assert scene.addTile( tll.Tile().setShapeRegular( (0.5, 0.866), 0.9, 6 ) ) == 4
    assert scene.addTile( tll.Tile().setShapeRegular( (-0.5, -0.866), 0.9, 6 ) ) == 5

    pablo.drawSceneTiles(scene)
    pablo.writeSceneTiles(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-11.svg" )
    
    scene.connectAll( [ [1, 2], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4] ] )

    pablo.drawSceneNetwork(scene)
    pablo.writeSceneTiles(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-12.svg" )
   
    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-13.svg" )

def test_artist_scene_net():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    scene.initializeSquares(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-14.svg" )

    box= [ (round(p.x(), 2), round(p.y(), 2)) for p in scene.box() ]
    assert box == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fitBox( scene.box() )
    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-15.svg" )

    scene.connectAllCondition(
        lambda tileFrom, tileTo : tileTo.matter() == 0 and tileFrom.centerDistance( tileTo ) < 1.2,
        lambda tileFrom : tileFrom.matter() == 0,
    )
    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-scene-16.svg" )


# Test artist on scene
def test_artist_scene_piece():
    pablo= tll.Artist().initializeSVG( filePath= shotImg )
    scene= tll.Scene()
    scene.initializeSquares(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )
    scene.connectAllCondition(
        lambda tileFrom, tileTo : tileFrom.centerDistance( tileTo ) < 1.2,
    )

    pablo.fitBox( scene.box() )
    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-01.svg" )

    scene.addPiece( hacka.Pod("R1.1"), 12, 13 )

    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-02.svg" )

    scene.addPiece(hacka.Pod("R1.1"),  9, 13)
    scene.addPiece(hacka.Pod("R2.2"), 14, 15)
    scene.addPiece(hacka.Pod("R1.2"), 23, 13)
    scene.addPiece(hacka.Pod("R2.1"), 20, 15)

    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-03.svg" )

    scene.addPiece(hacka.Pod("ViP1"), 17, 1)

    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-04.svg" )

    for tile in scene.tiles() :
        tile.clear()
    
    pablo.drawScene(scene)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-01.svg" )
