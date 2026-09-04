import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tild
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #
shotImg= "shot-test.svg"

# Test artist on tiles
def test_fast_tile_rendering():
    pablo= tild.createArtistSVG( shotImg, 800, 600 )
    tile= tild.Tile()
    
    tile.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-01.svg").read() )
    
    tile= tild.Tile( 3, 0, Convex().initSquare(4.0) )
    tile.setPosition(1.3, 0.9)
    tile.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-02.svg").read() )

    tile= tild.Tile(1, 1).setPosition(0.4, 0.2)
    tile.setShapeRegular( 2.0, 6 )
    tile.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-03.svg").read() )
    
    tile.renderOn( pablo )
    tile.writeOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-04.svg").read() )
    
# Test artist on tabletop
def test_fast_tabletop_tile_rendering():
    pablo= tild.createArtistSVG( shotImg, 800, 600 )
    tabletop= tild.Tabletop()

    assert tabletop.epsilon() == 0.01
        
    tabletop.renderTilesOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-00.svg" ).read() )

    tabletop= tild.Tabletop().initLine(3)

    assert tabletop.epsilon() == 0.01

    tabletop.renderTilesOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-01.svg" ).read() )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    tabletop.renderTilesOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-02.svg" ).read() )

def test_fast_tabletop_net_rendering():
    pablo= tild.createArtistSVG( shotImg, 800, 600 )
    tabletop= tild.Tabletop()
    tabletop.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [0, -1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 1, 0],
        [-1, -1, 0, 0, 0, -1, -1, -1]]
    )

    tabletop.renderOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-04.svg" ).read() )

    box= tabletop.box()
    box.round(2)
    assert box.asZip() == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fit( tabletop )
    tabletop.renderOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-05.svg" ).read() )

    tabletop.connectAllConditions(
        lambda tileFrom : tileFrom.group() == 0,
        lambda tileFrom, tileTo : tileTo.group() == 0 and tileFrom.centerDistance( tileTo ) < 1.2
    )
    tabletop.renderOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-06.svg" ).read() )


# Test artist on tabletop
def test_gridmap_piece():
    pablo= tild.createArtistSVG( shotImg, 800, 600 )
    tabletop= tild.Tabletop()
    tabletop.initGrid(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( tabletop.box() )
    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-01.svg" ).read() )

    def popEntity( iRobot, iGroup, iTile ):
        bob= tild.Entity( iGroup,
            tild.Convex().initRegular(0.7, 6),
            Point(0.1, 0.1)+tabletop.tile(iTile).position(),
            name= str(iRobot)
        )
        tabletop.tile(iTile).append( bob )
        return bob
    
    bob= popEntity(1, 13, 12)

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.referenceShape().asZipped() ]
    print( env )
    assert env == [
        (-0.3, -0.18), (-0.3, 0.17), (-0.0, 0.35),
        (0.3, 0.18), (0.3, -0.17), (0.0, -0.35),
    ]

    bob= tabletop.tile(12).entity()

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.projectedShape().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.projectedShape().asZipped() ]
    print( env )
    assert env == [
        (6.4, 3.23), (6.4, 3.58), (6.7, 3.75),
        (7.0, 3.58), (7.0, 3.23), (6.7, 3.05)
    ]
    

    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-02.svg" ).read() )
    
    popEntity(2, 13, 9)
    popEntity(2, 15, 14)
    popEntity(3, 13, 23)
    popEntity(1, 15, 20)

    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-03.svg" ).read() )

    popEntity(1, 1, 17)
    
    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-04.svg" ).read() )

    tabletop.clearEntities()
    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-01.svg" ).read() )

# Test artist on tabletop
def test_hexatabletop_piece():
    pablo= tild.createArtistSVG( shotImg, 800, 600 )
    tabletop= tild.Tabletop()
    tabletop.initHexa(
       [[0, 1, 1, -1, 0, 0, 0, 0],
        [5, -1, 0, 2, 0, -1, 5, 0],
        [0, 0, 0, -1, 0, 1, 1, 0],
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]],
        1.0, 0.1
    )

    pablo.fitBox( tabletop.box() )
    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-11.svg" ).read() )

    def popEntity( iRobot, iTile, iGroup ):
        bod= tild.Entity( iGroup,
            tild.Convex().initRegular(0.7, 6),
            Point(0.1, 0.1)+tabletop.tile(iTile).position(),
            name= str(iRobot)
        )
        tabletop.tile(iTile).append( bod )
    
    popEntity(1, 12, 13)

    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-12.svg" ).read() )
    
    popEntity(2,  9, 13)
    popEntity(2, 14, 15)
    popEntity(3, 23, 13)
    popEntity(1, 20, 15)

    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-13.svg" ).read() )

    popEntity(1, 17, 1)

    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-14.svg" ).read() )

    tabletop.clearEntities()
    tabletop.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-entity-11.svg" ).read() )


def test_gridtabletop_appendpiece():
    tabletop= tild.Tabletop()
    tabletop.initGrid([
        [0, 1, 1, -1, 0, 0, 0, 0], # -1 : means no cell at this selector
        [5, -1, 0, 2, 0, -1, 5, 0], # 0 - n : give the group identifier
        [0, 0, 0, -1, 0, 1, 1, 0], # of the cell to create.
        [0, 4, 0, -1, 0, 2, 1, 6],
        [-1, -1, 0, 0, 0, -1, -1, -1]
    ])

    tild.draw( tabletop, "shot-test.png", 800, 600 )
    tild.draw( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-01.svg" ).read() )

    # Add a first default entity on tile 2
    tabletop.tileAppendEntity( 2, tild.Entity() )

    tild.draw( tabletop, "shot-test.png", 800, 600 )
    tild.draw( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-02.svg" ).read() )

    # Add several entities associate to different groups...
    tabletop.tileAppendEntity( 8, tild.Entity(1) )
    tabletop.tileAppendEntity( 16, tild.Entity(1) )
    tabletop.tileAppendEntity( 4, tild.Entity(2) )
    tabletop.tileAppendEntity( 19, tild.Entity(2) )
    tabletop.tileAppendEntity( 24, tild.Entity(3) )
    tabletop.tileAppendEntity( 30, tild.Entity(3) )

    tild.draw( tabletop, "shot-test.png", 800, 600 )
    tild.draw( tabletop, "shot-test.svg", 800, 600 )

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.05-render-grid-03.svg" ).read() )
