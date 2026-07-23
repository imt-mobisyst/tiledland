# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Entity, Tile, Map 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #
def draw( entity ):
    tll.draw( entity, "shot-test.png", 800, 600 )

def test_fast_map_init():
    land= Map()
    assert type(land) == Map
    assert land.size() == 0
    assert land.box() == Box()

def test_fast_map_initLine():
    aMap= Map().initLine(3, connect=False)
    assert aMap.tile(1).index() == 1
    assert aMap.tile(2).index() == 2
    assert aMap.tile(3).index() == 3
    assert aMap.tiles() == [ aMap.tile(1), aMap.tile(2), aMap.tile(3) ]
    assert aMap.edges() == []

    assert aMap.tile(1).position().asTuple() == (0.0, 0.0)
    assert aMap.tile(1).projectedShape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert aMap.tile(2).position().asTuple() == (1.1, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in aMap.tile(2).projectedShape().asZipped() ]
    assert env == [(0.6, -0.5), (0.6, 0.5), (1.6, 0.5), (1.6, -0.5)]

    assert aMap.tile(3).position().asTuple() == (2.2, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in aMap.tile(3).projectedShape().asZipped() ]
    assert env == [(1.7, -0.5), (1.7, 0.5), (2.7, 0.5), (2.7, -0.5)]
    
def test_fast_map_construction():
    aMap= Map().initLine(3, connect=False)
    assert aMap.tile(1).adjacencies() == []
    assert aMap.tile(2).adjacencies() == []
    assert aMap.tile(3).adjacencies() == []
    aMap.connect(1, 2)
    aMap.connect(1, 3)
    aMap.connect(2, 2)
    aMap.connect(2, 1)
    aMap.connect(3, 1)
    aMap.connect(3, 2)
    aMap.connect(3, 3)
    assert aMap.tile(1).adjacencies() == [2, 3]
    assert aMap.tile(2).adjacencies() == [1, 2]
    assert aMap.tile(3).adjacencies() == [1, 2, 3]
    assert aMap.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idMap= id(aMap)
    aMap.initLine(3, connect=False)
    aMap.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {aMap.edges()}")
    assert( idMap == id(aMap) )
    assert aMap.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_fast_map_str():
    aMap= Map().initLine(3, connect=False)
    aMap.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    aMap.tile(2).append( Entity(1) )

    print( f">>> {aMap}." )

    assert "\n"+str(aMap)+"\n" == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(1)
  - Entity1 2-1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

def test_fast_map_hacka():
    aMap= Map().initLine(4, connect=False)
    aMap.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    aMap.tile(1).setPosition( 5.0, 3.0 )
    aMap.tile(2).setPosition( 5.0, 15.0 )
    aMap.tile(3).setPosition( 1.0, 9.0 )
    aMap.tile(4).setPosition( 9.0, 9.0 )

    print(f">>>\n{aMap}")
    assert '\n'+ str(aMap) +'\n' == """
Map:
- Tile-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] entities(0)
- Tile-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] entities(0)
- Tile-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] entities(0)
- Tile-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] entities(0)
"""

def test_fast_map_box():
    aMap= Map()
    assert aMap.box() == Box( [Point(0.0, 0.0)] )

    aMap= Map().initLine(4, connect=False)

    tll.draw( aMap, "shot-test.svg", 800, 600 )
    print( aMap.box() )
    assert str(aMap.box()) == "⌊(-0.5, -0.5), (3.8, 0.5)⌉"
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-line-01.svg", "r").read())

    aMap.initGrid( [[0, 1], [0, -1]] )

    tll.draw( aMap, "shot-test.svg", 800, 600 )
    print( aMap.box() )
    assert aMap.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-grid-01.svg", "r").read())

def test_fast_map_hacka():
    aMap= Map().initLine(3, connect=False)
    aMap.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    dt= aMap.asDataTree()

    assert dt.label() == "Map"

    assert dt.numberOfDigits() == 0
    assert dt.digits() == []
    
    assert dt.numberOfValues() == 1
    assert dt.values() == [0.01]
    
    assert dt.numberOfChildren() == 3
    assert dt.children() == [ t.asDataTree() for t in aMap.tiles() ]

def test_fast_map_DataTreecopy():
    aMap= Map().initLine(3, connect=False)
    aMap.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert aMap.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    print( '>>>\n'+ str(aMap) +'\n---')

    assert '\n'+ str(aMap) +'\n' == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    print("Go for the copying...")
    mapBis= aMap.dataTreeCopy()
    aMap.connect(3, 1)

    assert type(aMap) == type(mapBis)
    assert mapBis.size() == 3

    print(f">>>\n{mapBis}")
    assert '\n'+ str(mapBis) +'\n' == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert mapBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_fast_map_connection():
    aMap= Map().initLine( 3, connect=False )
    aMap.connect(1, 2)
    aMap.connect(2, 2)
    aMap.connect(2, 3)
    aMap.connect(3, 2)
    print( f">>>\n{map}\n---")
    assert "\n"+ str(aMap) +"\n"  == """
Map:
- Tile0 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] entities(0)
- Tile0 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] entities(0)
- Tile0 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert aMap.tile(1).adjacencies() == [2]
    assert aMap.tile(2).adjacencies() == [2, 3]
    assert aMap.tile(3).adjacencies() == [2]
    
    assert aMap.isEdge(1, 2)
    assert aMap.isEdge(2, 2)
    assert aMap.isEdge(3, 2)
    assert not aMap.isEdge(2, 1)
    assert not aMap.isEdge(1, 3)
    assert not aMap.isEdge(3, 1)
  
def test_fast_map_withEntities():
    aMap= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert aMap.numberOfEntities() == 0
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 0
    assert aMap.tile(3).numberOfEntities() == 0
    
    aMap.tileAppendEntity(2)

    assert aMap.numberOfEntities() == 1
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 1
    assert aMap.tile(3).numberOfEntities() == 0

    aMap.tileAppendEntity(1)

    assert aMap.numberOfEntities() == 2
    assert aMap.tile(1).numberOfEntities() == 1
    assert aMap.tile(2).numberOfEntities() == 1
    assert aMap.tile(3).numberOfEntities() == 0

    bod= aMap.tileAppendEntity(2)

    assert aMap.numberOfEntities() == 3
    assert aMap.tile(1).numberOfEntities() == 1
    assert aMap.tile(2).numberOfEntities() == 2
    assert aMap.tile(3).numberOfEntities() == 0

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] entities(1)
  - Entity0 1-1 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile1 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] entities(2)
  - Entity0 2-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Entity0 2-2 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile0 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] entities(0)"""

    aMap.clearEntities()

    assert aMap.numberOfEntities() == 0
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 0
    assert aMap.tile(3).numberOfEntities() == 0

def test_fast_map_popEntities():
    aMap= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert aMap.numberOfEntities() == 0
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 0
    assert aMap.tile(3).numberOfEntities() == 0
    
    bod= aMap.tileAppendEntity(2)

    assert type(bod) == Entity
    assert bod.location() == (2, 1)
    assert aMap.eEentity(2, 1) == bod

    assert aMap.numberOfEntities() == 1
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 1
    assert aMap.tile(3).numberOfEntities() == 0

    bod= aMap.tileAppendEntity(1)

    assert type(bod) == Entity
    assert bod.location() == (1, 1)
    assert aMap.eEentity(1, 1) == bod

    bod= aMap.tileAppendEntity(1)

    assert type(bod) == Entity
    assert bod.location() == (1, 2)
    assert aMap.eEentity(1, 1) != bod
    assert aMap.eEentity(1, 2) == bod

    assert aMap.numberOfEntities() == 3
    assert aMap.tile(1).numberOfEntities() == 2
    assert aMap.tile(2).numberOfEntities() == 1
    assert aMap.tile(3).numberOfEntities() == 0

    bod= aMap.tileAppendEntity(2)

    assert aMap.numberOfEntities() == 4
    assert aMap.tile(1).numberOfEntities() == 2
    assert aMap.tile(2).numberOfEntities() == 2
    assert aMap.tile(3).numberOfEntities() == 0

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] entities(2)
  - Entity0 1-1 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
  - Entity0 1-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile1 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] entities(2)
  - Entity0 2-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Entity0 2-2 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile0 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] entities(0)"""

    aMap.clearEntities()

    assert aMap.numberOfEntities() == 0
    assert aMap.tile(1).numberOfEntities() == 0
    assert aMap.tile(2).numberOfEntities() == 0
    assert aMap.tile(3).numberOfEntities() == 0

def test_fast_map_moveEntities():
    aMap= Map().initGrid( [[0, 0, 1],[-1, 0, 0], [2, 0, -1]] )
    draw(aMap)

    c= 1
    entShape= Convex().initArrowTip(0.4)
    for i in [1, 1, 2, 2, 3] :
        aMap.tileAppendEntity(i, Entity(shape=entShape, name= f"E.{c}")  )
        c+= 1

    draw(aMap)
    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - E.10 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.20 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile0 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(2)
  - E.30 2-1 ⌊(0.93, 2.0), (1.3, 2.4)⌉
  - E.40 2-2 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- Tile1 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - E.50 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile0 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- Tile0 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- Tile2 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- Tile0 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= aMap.tileRemoveEntity(2, 1)

    print( bob )
    assert str(bob) == "E.30 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - E.10 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.20 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile0 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(1)
  - E.40 2-1 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- Tile1 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - E.50 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile0 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- Tile0 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- Tile2 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- Tile0 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""
    
    bob= aMap.tileRemoveEntity(2, 1)

    print( bob )
    assert str(bob) == "E.40 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - E.10 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.20 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile0 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- Tile1 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - E.50 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile0 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- Tile0 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- Tile2 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- Tile0 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= aMap.moveEntity(3, 1, 1)

    print( bob )
    assert bob.name() == "E.5"
    assert bob.location() == (1, 3)

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(3)
  - E.10 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.20 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.50 1-3 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile0 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- Tile1 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(0)
- Tile0 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- Tile0 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- Tile2 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- Tile0 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= aMap.moveEntity(1, 2, 4)

    print( bob )
    assert bob.name() == "E.2"
    assert bob.location() == (4, 1)

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile0 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - E.10 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - E.50 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile0 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- Tile1 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(0)
- Tile0 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(1)
  - E.20 4-1 ⌊(0.93, 0.9), (1.3, 1.3)⌉
- Tile0 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- Tile2 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- Tile0 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""
