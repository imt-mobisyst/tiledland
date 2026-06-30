# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Agent, Tile, Map 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_map_init():
    land= Map()
    assert type(land) == Map
    assert land.size() == 0
    assert land.box() == Box()

def test_fast_map_initLine():
    aMap= Map().initLine(3, connect=False)
    assert aMap.tile(1).id() == 1
    assert aMap.tile(2).id() == 2
    assert aMap.tile(3).id() == 3
    assert aMap.tiles() == [ aMap.tile(1), aMap.tile(2), aMap.tile(3) ]
    assert aMap.edges() == []

    assert aMap.tile(1).position().asTuple() == (0.0, 0.0)
    assert aMap.tile(1).body().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert aMap.tile(2).position().asTuple() == (1.1, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in aMap.tile(2).body().asZipped() ]
    assert env == [(0.6, -0.5), (0.6, 0.5), (1.6, 0.5), (1.6, -0.5)]

    assert aMap.tile(3).position().asTuple() == (2.2, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in aMap.tile(3).body().asZipped() ]
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
    aMap.tile(2).append( Agent(1, 1) )

    print( f">>> {aMap}." )

    assert "\n"+str(aMap)+"\n" == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] agents(1)
  - Agent-1.1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] agents(0)
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
- Tile-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ matter-0 adjs[2, 3, 4] agents(0)
- Tile-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ matter-0 adjs[1, 3, 4] agents(0)
- Tile-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ matter-0 adjs[1, 2] agents(0)
- Tile-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ matter-0 adjs[1, 2] agents(0)
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
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] agents(0)
"""

    print("Go for the copying...")
    mapBis= aMap.dataTreeCopy()
    aMap.connect(3, 1)

    assert type(aMap) == type(mapBis)
    assert mapBis.size() == 3

    print(f">>>\n{mapBis}")
    assert '\n'+ str(mapBis) +'\n' == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] agents(0)
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
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] agents(0)
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
  
def test_fast_map_withAgents():
    aMap= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert aMap.testNumberOfAgents() == 0
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 0
    assert aMap.tile(3).count() == 0
    
    aMap.popAgentOn(2)

    assert aMap.testNumberOfAgents() == 1
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 1
    assert aMap.tile(3).count() == 0

    aMap.popAgentOn(1)

    assert aMap.testNumberOfAgents() == 2
    assert aMap.tile(1).count() == 1
    assert aMap.tile(2).count() == 1
    assert aMap.tile(3).count() == 0

    bod= aMap.popAgentOn(2)
    bod.setId(4)

    assert aMap.testNumberOfAgents() == 3
    assert aMap.tile(1).count() == 1
    assert aMap.tile(2).count() == 2
    assert aMap.tile(3).count() == 0

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] agents(1)
  - Agent-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile-1.2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] agents(2)
  - Agent-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Agent-4 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] agents(0)"""

    aMap.clearAgents()

    assert aMap.testNumberOfAgents() == 0
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 0
    assert aMap.tile(3).count() == 0

def test_fast_map_popAgents():
    aMap= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert aMap.testNumberOfAgents() == 0
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 0
    assert aMap.tile(3).count() == 0
    
    bod= aMap.popAgentOn(2)

    assert type(bod) == Agent
    assert bod.id() == 1
    assert aMap.agent(1) == bod

    assert aMap.testNumberOfAgents() == 1
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 1
    assert aMap.tile(3).count() == 0

    bod= aMap.popAgentOn(1)

    assert type(bod) == Agent
    assert bod.id() == 2
    assert aMap.agent(2) == bod

    assert aMap.testNumberOfAgents() == 2
    assert aMap.tile(1).count() == 1
    assert aMap.tile(2).count() == 1
    assert aMap.tile(3).count() == 0

    bod= aMap.popAgentOn(2)

    assert aMap.testNumberOfAgents() == 3
    assert aMap.tile(1).count() == 1
    assert aMap.tile(2).count() == 2
    assert aMap.tile(3).count() == 0

    print( f"---\n{aMap}.")
    assert str(aMap) == """Map:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] agents(1)
  - Agent-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile-1.2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] agents(2)
  - Agent-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Agent-3 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] agents(0)"""

    aMap.clearAgents()

    assert aMap.testNumberOfAgents() == 0
    assert aMap.tile(1).count() == 0
    assert aMap.tile(2).count() == 0
    assert aMap.tile(3).count() == 0