import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tild
from src.tiledland.geometry import Point, Convex
from src.tiledland.artist import Brush

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #
shotImg= "shot-test.svg"

# Test artist on tiles
def test_fast_tile_rendering():
    pablo= tild.artist.openSVG( shotImg, 800, 600 )
    assert type(pablo) == tild.artist.ArtistBasic

    tile= tild.Tile( category=0 )
    assert tile.position().asTuple() == (0.0, 0.0)
    assert str(tile) == "Tile 0-0 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[] units(0)"
    
    pablo.drawTile(tile)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-01.svg").read() )
    
    tile= tild.Tile( Convex().initSquare(4.0), category= 0 )
    tile.setPosition( Point(1.3, 0.9) )
    pablo.drawTile(tile)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-02.svg").read() )

    tile= tild.Tile( index= 1).setCategory(1)
    tile.setShape( tild.Convex().initRegular( 2.0, 6 ) )
    tile.setPosition( Point(0.4, 0.2) )
    pablo.drawTile(tile)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-03.svg").read() )
    
    pablo.drawTile(tile)
    pablo.tagTile(tile, str(tile.index()))
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-04.svg").read() )
    
# Test artist on tabletop
def test_fast_tabletop_tile_rendering():
    pablo= tild.artist.openSVG( shotImg, 800, 600 )
    tabletop= tild.Map()

    assert tabletop.epsilon() == 0.01
        
    pablo.drawMapTiles(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-00.svg" ).read() )

    tabletop= tild.Map().initLine(3)

    assert tabletop.epsilon() == 0.01

    pablo.drawMapTiles(tabletop)
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-01.svg" ).read() )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    pablo.drawMapTiles(tabletop)
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-02.svg" ).read() )

def test_fast_tabletop_net_rendering():
    pablo= tild.artist.openSVG( shotImg, 800, 600 )
    pablo.setScale(100.0)
    tabletop= tild.Map()
    tabletop.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-04.svg" ).read() )

    box= tabletop.box()
    box.round(2)
    assert box.asZip() == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fit( tabletop )
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-05.svg" ).read() )

    cat= tabletop.tile(1).category()
    tabletop.connectAllConditions(
        lambda tileFrom : tileFrom.category() == cat,
        lambda tileFrom, tileTo : tileTo.category() == 0 and tileFrom.centerDistance( tileTo ) < 1.2
    )
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-06.svg" ).read() )


# Test artist on tabletop
def test_gridmap_piece():
    pablo= tild.artist.openSVG( shotImg, 800, 600 )
    tabletop= tild.Map()
    tabletop.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( tabletop.box() )
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-01.svg" ).read() )

    def popUnit( iRobot, iGroup, iTile ):
        bob= tild.Unit( tild.Convex().initRegular(0.7, 6), owner= iGroup )
        bob.setPosition( Point(0.1, 0.1)+tabletop.tile(iTile).position() )
        bob.setName( str(iRobot) )
        tabletop.tile(iTile).append( bob )
        return bob
    
    bob= popUnit(1, 13, 12)

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.outline().asZipped() ]
    print( env )
    assert env == [
        (-0.3, -0.18), (-0.3, 0.17), (-0.0, 0.35),
        (0.3, 0.18), (0.3, -0.17), (0.0, -0.35),
    ]

    bob= tabletop.tile(12).unit()

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.shape().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.shape().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]
    

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-02.svg" ).read() )
    
    popUnit(2, 13, 9)
    popUnit(2, 15, 14)
    popUnit(3, 13, 23)
    popUnit(1, 15, 20)

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-03.svg" ).read() )

    popUnit(1, 11, 17)
    
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-04.svg" ).read() )

    tabletop.clearUnits()
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-01.svg" ).read() )

# Test artist on tabletop
def test_hexatabletop_piece():
    pablo= tild.artist.openSVG( shotImg, 800, 600 )
    tabletop= tild.Map()
    tabletop.initHexa(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( tabletop.box() )
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-11.svg" ).read() )

    def popUnit( iRobot, iTile, iGroup ):
        bob= tild.Unit( tild.Convex().initRegular(0.7, 6) )
        bob.setPosition( Point(0.1, 0.1)+tabletop.tile(iTile).position() )
        bob.setOwner(iGroup)
        bob.setName( str(iRobot) )
        tabletop.tile(iTile).append( bob )
        return bob
    
    popUnit(1, 12, 13)

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-12.svg" ).read() )
    
    popUnit(2,  9, 13)
    popUnit(2, 14, 15)
    popUnit(3, 23, 13)
    popUnit(1, 20, 15)

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-13.svg" ).read() )

    popUnit(1, 17, 1)

    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-14.svg" ).read() )

    tabletop.clearUnits()
    pablo.drawMap(tabletop)
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-11.svg" ).read() )


def test_gridtabletop_appendMobiles():
    tabletop= tild.Map()
    tabletop.initGrid([
        [0, 1, 1, -1, 0, 0, 0, 0], # -1 : means no cell at this selector
        [5, -1, 0, 2, 0, -1, 5, 0], # 0 - n : give the group identifier
        [0, 0, 0, -1, 0, 1, 1, 0], # of the cell to create.
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]
    ])

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-01.svg" ).read() )

    # Add a first default entity on tile 2
    mobile= tild.Unit(Convex().initArrowTip(1.0), owner= 10, name="Mobile")
    tabletop.tileAppendUnit( 2, mobile.copy() )

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-02.svg" ).read() )

    # Add several units associate to different groups...
    tabletop.tileAppendUnit( 8, mobile.copy().setOwner(11) )
    tabletop.tileAppendUnit( 16, mobile.copy().setOwner(11) )
    tabletop.tileAppendUnit( 4, mobile.copy().setOwner(12) )
    tabletop.tileAppendUnit( 19, mobile.copy().setOwner(12) )
    tabletop.tileAppendUnit( 24, mobile.copy().setOwner(13) )
    tabletop.tileAppendUnit( 30, mobile.copy().setOwner(13) )

    tild.drawMap( tabletop, "shot-test.png", 800, 600 )
    tild.drawMap( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-03.svg" ).read() )
