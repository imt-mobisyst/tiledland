import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll
from src.tiledland.geometry import Point, Convex, Box
from src.tiledland import Entity, Tile, Map

# ----------------------------------------------------------------------- #
#           T E S T   T I L E D L A N D - I N T E G R A T E D   
# ----------------------------------------------------------------------- #

def draw(map, filePath= "shot-test.png"):
    pablo= tll.createArtistPNG( filePath, 800, 600 )
    
    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    map.renderNetworkOn(pablo)
    map.renderTilesOn(pablo)

    pablo.flip()

def test_map_incremental():
    map= Map()
    
    assert type(map) == Map
    assert map.size() == 0
    assert map.box() == Box()

    index= map.appendTile( Tile( shape= Convex() ) ).index()
    assert index == 1
    assert map.size() == 1

    print( map.tile(1) )
    assert map.tile(1).position().asTuple() == (0.0, 0.0)
    assert map.tile(1).projectedShape().asZipped() == []

    index= map.appendTile( Tile( shape= Convex() ) ).index()
    assert index == 2
    assert map.size() == 2

def test_map_clockNeighboring():
    map= Map()
    tileConvex= Convex().fromZipped(
        [(-1.0, 0.0), (0.0, 1.5), (1.0, 0.0), (0.0, -1.5) ]
    )
    map.appendTile( Tile( shape=tileConvex, group= 1 ) )

    draw(map)

    assert map.neighbours(1) == []

    t= map.appendTile( Tile( shape= tileConvex, position=Point(1.5, 2), group= 2 ) )
    map.connect( 1, t.index() )    
    assert map.neighbours(1) == [(2, 1)]
    draw(map)

    t= map.appendTile( Tile( shape= tileConvex, position=Point(-1.5, 2), group= 2 ) )
    map.connect( 1, t.index() )    
    draw(map)
    assert map.neighbours(1) == [(2, 1), (3, 11)]

    t= map.appendTile( Tile( shape= tileConvex, position=Point(1.5, -2), group= 2 ) )
    map.connect( 1, t.index() )    
    t= map.appendTile( Tile( shape= tileConvex, position=Point(-1.5, -2), group= 2 ) )
    map.connect( 1, t.index() )    
    draw(map)
    assert map.neighbours(1) == [(2, 1), (3, 11), (4, 5), (5, 7)]

    assert map.tile(1).adjacencies() == [2, 3, 4, 5]
    assert map.edges() == [(1, 2), (1, 3), (1, 4), (1, 5)]

def test_Map_initLine():
    map= Map().initLine(3, connect=False)
    assert map.tile(1).index() == 1
    assert map.tile(2).index() == 2
    assert map.tile(3).index() == 3
    assert map.tiles() == [ map.tile(1), map.tile(2), map.tile(3) ]
    assert map.edges() == []

    assert map.tile(1).position().asTuple() == (0.0, 0.0)
    assert map.tile(1).projectedShape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert map.tile(2).position().asTuple() == (1.1, 0.0)
    assert map.tile(3).position().asTuple() == (2.2, 0.0)
    
def test_Map_construction():
    map= Map().initLine(3, connect=False)
    assert map.tile(1).adjacencies() == []
    assert map.tile(2).adjacencies() == []
    assert map.tile(3).adjacencies() == []
    map.connect(1, 2)
    map.connect(1, 3)
    map.connect(2, 2)
    map.connect(2, 1)
    map.connect(3, 1)
    map.connect(3, 2)
    map.connect(3, 3)
    assert map.tile(1).adjacencies() == [2, 3]
    assert map.tile(2).adjacencies() == [1, 2]
    assert map.tile(3).adjacencies() == [1, 2, 3]
    assert map.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idMap= id(map)
    map.initLine(3, connect=False)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {map.edges()}")
    assert( idMap == id(map) )
    assert map.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_Map_str():
    map= Map().initLine(3, connect=False)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    map.tile(2).append( Entity(1) )

    print( f">>>\n{map}." )

    assert "\n"+str(map)+"\n" == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(1)
  - Entity1 2-1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

def test_Map_hacka():
    map= Map().initLine(4, connect=False)
    map.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    map.tile(1).setPosition( 5.0, 3.0 )
    map.tile(2).setPosition( 5.0, 15.0 )
    map.tile(3).setPosition( 1.0, 9.0 )
    map.tile(4).setPosition( 9.0, 9.0 )

    print(f">>>\n{map}.")
    assert '\n'+ str(map) +'\n' == """
Map:
- Tile0 0-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] entities(0)
- Tile0 0-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] entities(0)
- Tile0 0-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] entities(0)
- Tile0 0-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] entities(0)
"""

def test_Map_box():
    map= Map()
    assert map.box() == Box( [Point(0.0, 0.0)] )

    map= Map().initLine(4, connect=False)
    box= map.box()
    print(box)
    box.round(3)
    assert box.asZip() == [(-0.5, -0.5), (3.8, 0.5)]
    
    map.initGrid( [[0, 1], [0, -1]] )
    print( map.box() )
    assert map.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]

def test_Map_hacka2():
    map= Map().initLine(3, connect=False)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    dt= map.asDataTree()

    assert dt.label() == "Map"

    assert dt.numberOfDigits() == 0
    assert dt.digits() == []
    
    assert dt.numberOfValues() == 1
    assert dt.values() == [0.01]
    
    assert dt.numberOfChildren() == 3
    assert dt.children() == [ t.asDataTree() for t in map.tiles() ]

def test_Map_dataTreecopy():
    map= Map().initLine(3, connect=False)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert map.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]
    print( f">>>\n{map}." )
    assert '\n'+ str(map) +'\n' == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    print("Go for the copying...")
    mapBis= map.dataTreeCopy()
    map.connect(3, 1)

    assert type(map) == type(mapBis)
    assert mapBis.size() == 3

    print(f">>>\n{mapBis}.")
    assert '\n'+ str(mapBis) +'\n' == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert mapBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_Map_connection():
    map= Map().initLine(3, connect=False)
    map.connect(1, 2)
    map.connect(2, 2)
    map.connect(2, 3)
    map.connect(3, 2)
    print( f">>>\n{map}.")
    assert "\n"+ str(map) +"\n" == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert map.tile(1).adjacencies() == [2]
    assert map.tile(2).adjacencies() == [2, 3]
    assert map.tile(3).adjacencies() == [2]
    
    assert map.isEdge(1, 2)
    assert map.isEdge(2, 2)
    assert map.isEdge(3, 2)
    assert not map.isEdge(2, 1)
    assert not map.isEdge(1, 3)
    assert not map.isEdge(3, 1)

def test_Map_hexa():
    map= Map().initHexa(
        [[-1, 0],
           [1, 0],
         [0, -1]]
    )
    draw(map)
    print( f"---\n{map}.")
    assert str(map) == """Map:
- Tile0 0-1 ⌊(0.53, 1.17), (1.4, 2.17)⌉ adjs[2, 3] entities(0)
- Tile1 0-2 ⌊(0.05, 0.34), (0.92, 1.34)⌉ adjs[1, 3, 4] entities(0)
- Tile0 0-3 ⌊(1.02, 0.34), (1.88, 1.34)⌉ adjs[1, 2] entities(0)
- Tile0 0-4 ⌊(-0.43, -0.5), (0.43, 0.5)⌉ adjs[2] entities(0)"""