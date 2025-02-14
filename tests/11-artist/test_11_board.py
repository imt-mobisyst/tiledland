import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import hacka.py as hacka
import src.tiledland.artist as hka
import src.tiledland as hkb

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
    pablo= hka.Artist().initializeSVG( filePath= shotImg )
    tile= hkb.Tile()
    
    pablo.drawTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-01.svg" )

    tile= hkb.Tile( 3, 0, hkb.Float2(1.3, 0.9), 4.0 )
    pablo.drawTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-02.svg" )

    tile= hkb.Tile( 1, 1 ).setCenter( 0.4, 0.2 ).setShapeRegular( 2.0, 6 )
    pablo.drawTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-03.svg" )

    pablo.drawTile( tile )
    pablo.writeTile( tile )
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-tile-04.svg" )

# Test artist on map
def test_artist_map_tiles():
    pablo= hka.Artist().initializeSVG( filePath= shotImg )
    map= hkb.Map()
    
    pablo.drawMapTiles(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-00.svg" )
    
    map= hkb.Map().initializeLine(3)

    pablo.drawMapTiles(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-01.svg" )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    pablo.drawMapTiles(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-02.svg" )

def test_artist_map_net():
    pablo= hka.Artist( hka.SupportSVG( filePath= shotImg ) )
    map= hkb.Map()
    
    assert map.addTile( hkb.Tile().setShapeRegular( (-1.0, 0.0), 0.9, 6 ) ) == 1
    assert map.addTile( hkb.Tile( type=1 ).setShapeRegular( (0.0, 0.0), 0.9, 6 ) ) == 2
    assert map.addTile( hkb.Tile().setShapeRegular( (1.0, 0.0), 0.9, 6 ) ) == 3

    assert map.addTile( hkb.Tile().setShapeRegular( (0.5, 0.866), 0.9, 6 ) ) == 4
    assert map.addTile( hkb.Tile().setShapeRegular( (-0.5, -0.866), 0.9, 6 ) ) == 5

    pablo.drawMapTiles(map)
    pablo.writeMapTiles(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-11.svg" )
    
    map.connectAll( [ [1, 2], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4] ] )

    pablo.drawMapNetwork(map)
    pablo.writeMapTiles(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-12.svg" )
   
    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-13.svg" )

def test_artist_map_net():
    pablo= hka.Artist().initializeSVG( filePath= shotImg )
    map= hkb.Map()
    map.initializeSquares(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-14.svg" )

    box= [ (round(p.x(), 2), round(p.y(), 2)) for p in map.box() ]
    assert box == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fitBox( map.box() )
    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-15.svg" )

    map.connectAllCondition(
        lambda tileFrom, tileTo : tileTo.matter() == 0 and tileFrom.centerDistance( tileTo ) < 1.2,
        lambda tileFrom : tileFrom.matter() == 0,
    )
    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-map-16.svg" )


# Test artist on map
def test_artist_map_piece():
    pablo= hka.Artist().initializeSVG( filePath= shotImg )
    map= hkb.Map()
    map.initializeSquares(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )
    map.connectAllCondition(
        lambda tileFrom, tileTo : tileFrom.centerDistance( tileTo ) < 1.2,
    )

    pablo.fitBox( map.box() )
    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-01.svg" )

    map.addPiece( hacka.Pod("R1.1"), 12, 13 )

    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-02.svg" )

    map.addPiece(hacka.Pod("R1.1"),  9, 13)
    map.addPiece(hacka.Pod("R2.2"), 14, 15)
    map.addPiece(hacka.Pod("R1.2"), 23, 13)
    map.addPiece(hacka.Pod("R2.1"), 20, 15)

    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-03.svg" )

    map.addPiece(hacka.Pod("ViP1"), 17, 1)

    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-04.svg" )

    for tile in map.tiles() :
        tile.clear()
    
    pablo.drawMap(map)
    pablo.flip()

    compareSvg( shotImg, "tests/refs/11.11-artist-piece-01.svg" )
