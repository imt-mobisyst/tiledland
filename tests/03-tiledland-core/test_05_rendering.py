import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tll
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #
shotImg= "shot-test.svg"

# Test artist on tiles
def test_fast_tile_rendering():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    tile= tll.Tile()
    
    tile.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-01.svg").read() )
    
    tile= tll.Tile( 3, 0, Convex().initSquare(4.0) )
    tile.setPosition(1.3, 0.9)
    tile.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-tile-02.svg").read() )

    tile= tll.Tile(1, 1).setPosition(0.4, 0.2)
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
    
# Test artist on map
def test_fast_map_tile_rendering():
    pablo= tll.createArtistSVG( shotImg, 800, 600 )
    map= tll.Map()

    assert map.epsilon() == 0.01
        
    map.renderTilesOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-00.svg" ).read() )

    map= tll.Map().initLine(3)

    assert map.epsilon() == 0.01

    map.renderTilesOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-01.svg" ).read() )

    pablo.setCamera( 1.1, 0.0 )
    pablo.setScale( 200 )

    map.renderTilesOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-02.svg" ).read() )

def test_fast_map_net_rendering():
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


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-04.svg" ).read() )

    box= map.box()
    box.round(2)
    assert box.asZip() == [(-0.5, -0.5), (8.2, 4.9)] 

    pablo.fit( map )
    map.renderOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-05.svg" ).read() )

    map.connectAllConditions(
        lambda tileFrom : tileFrom.group() == 0,
        lambda tileFrom, tileTo : tileTo.group() == 0 and tileFrom.centerDistance( tileTo ) < 1.2
    )
    map.renderOn( pablo )
    pablo.flip()


    assert( open(shotImg).read()
        == open("tests/refs/03.05-map-06.svg" ).read() )


# Test artist on map
def test_gridmap_piece():
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

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-01.svg" ).read() )

    def popAgent( iRobot, iGroup, iTile ):
        bob= tll.Agent( iRobot, iGroup,
            tll.Convex().initRegular(0.7, 6),
            Point(0.1, 0.1)+map.tile(iTile).position()
        )
        map.tile(iTile).append( bob )
        return bob
    
    bob= popAgent(1, 13, 12)

    env= [ ( round(x, 2), round(y, 2) ) for x, y in bob.referenceShape().asZipped() ]
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

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-02.svg" ).read() )
    
    popAgent(2, 13, 9)
    popAgent(2, 15, 14)
    popAgent(3, 13, 23)
    popAgent(1, 15, 20)

    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-03.svg" ).read() )

    popAgent(1, 1, 17)
    
    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-04.svg" ).read() )

    map.clearAgents()
    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-01.svg" ).read() )

# Test artist on map
def test_hexamap_piece():
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

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-11.svg" ).read() )

    def popAgent( iRobot, iTile, iGroup ):
        bod= tll.Agent( iRobot, iGroup,
            tll.Convex().initRegular(0.7, 6),
            Point(0.1, 0.1)+map.tile(iTile).position()
        )
        map.tile(iTile).append( bod )
    
    popAgent(1, 12, 13)

    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-12.svg" ).read() )
    
    popAgent(2,  9, 13)
    popAgent(2, 14, 15)
    popAgent(3, 23, 13)
    popAgent(1, 20, 15)

    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-13.svg" ).read() )

    popAgent(1, 17, 1)

    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-14.svg" ).read() )

    map.clearAgents()
    map.renderOn( pablo )
    pablo.flip()

    assert( open(shotImg).read()
        == open("tests/refs/03.05-agent-11.svg" ).read() )
