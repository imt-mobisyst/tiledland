# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Agent, Tile, Map 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Map_init():
    map= Map()
    assert type(map) == Map
    assert map.size() == 0
    assert map.box() == Box()

def test_Map_initLine():
    map= Map().initLine(3, connect=False)
    assert map.tile(1).id() == 1
    assert map.tile(2).id() == 2
    assert map.tile(3).id() == 3
    assert map.tiles() == [ map.tile(1), map.tile(2), map.tile(3) ]
    assert map.edges() == []

    assert map.tile(1).position().asTuple() == (0.0, 0.0)
    assert map.tile(1).body().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert map.tile(2).position().asTuple() == (1.1, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in map.tile(2).body().asZipped() ]
    assert env == [(0.6, -0.5), (0.6, 0.5), (1.6, 0.5), (1.6, -0.5)]

    assert map.tile(3).position().asTuple() == (2.2, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in map.tile(3).body().asZipped() ]
    assert env == [(1.7, -0.5), (1.7, 0.5), (2.7, 0.5), (2.7, -0.5)]
    
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
    map.tile(2).append( Agent(1, 1) )

    print( f">>> {map}." )

    assert "\n"+str(map)+"\n" == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ matter-0 adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[1, 2] agents(1)
  - Agent-1.1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ matter-0 adjs[2] agents(0)
"""

def test_Map_hacka():
    map= Map().initLine(4, connect=False)
    map.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    map.tile(1).position().set( 5.0, 3.0 )
    map.tile(2).position().set( 5.0, 15.0 )
    map.tile(3).position().set( 1.0, 9.0 )
    map.tile(4).position().set( 9.0, 9.0 )

    print(f">>>\n{map}")
    assert '\n'+ str(map) +'\n' == """
Map:
- Tile-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ matter-0 adjs[2, 3, 4] agents(0)
- Tile-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ matter-0 adjs[1, 3, 4] agents(0)
- Tile-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ matter-0 adjs[1, 2] agents(0)
- Tile-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ matter-0 adjs[1, 2] agents(0)
"""

def test_Map_box():
    map= Map()
    assert map.box() == Box( [Point(0.0, 0.0)] )

    map= Map().initLine(4, connect=False)
    print( map.box() )
    assert str(map.box()) == "⌊(-0.5, -0.5), (3.8, 0.5)⌉"
    
    map.initGrid( [[0, 1], [0, -1]] )
    print( map.box() )
    assert map.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]

def test_Map_hacka():
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

def test_Map_DataTreecopy():
    map= Map().initLine(3, connect=False)
    map.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert map.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    print( '>>>\n'+ str(map) +'\n---')

    assert '\n'+ str(map) +'\n' == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ matter-0 adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[1, 2] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ matter-0 adjs[2] agents(0)
"""

    print("Go for the copying...")
    mapBis= map.dataTreeCopy()
    map.connect(3, 1)

    assert type(map) == type(mapBis)
    assert mapBis.size() == 3

    print(f">>>\n{mapBis}")
    assert '\n'+ str(mapBis) +'\n' == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ matter-0 adjs[1, 3] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[1, 2] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ matter-0 adjs[2] agents(0)
"""

    assert mapBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_Map_connection():
    map= Map().initLine( 3, connect=False )
    map.connect(1, 2)
    map.connect(2, 2)
    map.connect(2, 3)
    map.connect(3, 2)
    print( f">>>\n{map}\n---")
    assert "\n"+ str(map) +"\n"  == """
Map:
- Tile-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ matter-0 adjs[2] agents(0)
- Tile-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[2, 3] agents(0)
- Tile-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ matter-0 adjs[2] agents(0)
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
  
def test_Map_withAgents():
    map= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert map.testNumberOfAgents() == 0
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 0
    assert map.tile(3).count() == 0
    
    map.popAgentOn(2)

    assert map.testNumberOfAgents() == 1
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 1
    assert map.tile(3).count() == 0

    map.popAgentOn(1)

    assert map.testNumberOfAgents() == 2
    assert map.tile(1).count() == 1
    assert map.tile(2).count() == 1
    assert map.tile(3).count() == 0

    bod= map.popAgentOn(2)
    bod.setId(4)

    assert map.testNumberOfAgents() == 3
    assert map.tile(1).count() == 1
    assert map.tile(2).count() == 2
    assert map.tile(3).count() == 0

    print( f"---\n{map}.")
    assert str(map) == """Map:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ matter-0 adjs[2] agents(1)
  - Agent-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ matter-1 adjs[1, 3] agents(2)
  - Agent-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Agent-4 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[2] agents(0)"""

    map.clearAgents()

    assert map.testNumberOfAgents() == 0
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 0
    assert map.tile(3).count() == 0

def test_Map_popAgents():
    map= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert map.testNumberOfAgents() == 0
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 0
    assert map.tile(3).count() == 0
    
    bod= map.popAgentOn(2)

    assert type(bod) == Agent
    assert bod.id() == 1
    assert map.agent(1) == bod

    assert map.testNumberOfAgents() == 1
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 1
    assert map.tile(3).count() == 0

    bod= map.popAgentOn(1)

    assert type(bod) == Agent
    assert bod.id() == 2
    assert map.agent(2) == bod

    assert map.testNumberOfAgents() == 2
    assert map.tile(1).count() == 1
    assert map.tile(2).count() == 1
    assert map.tile(3).count() == 0

    bod= map.popAgentOn(2)

    assert map.testNumberOfAgents() == 3
    assert map.tile(1).count() == 1
    assert map.tile(2).count() == 2
    assert map.tile(3).count() == 0

    print( f"---\n{map}.")
    assert str(map) == """Map:
- Tile-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ matter-0 adjs[2] agents(1)
  - Agent-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- Tile-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ matter-1 adjs[1, 3] agents(2)
  - Agent-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - Agent-3 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- Tile-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ matter-0 adjs[2] agents(0)"""

    map.clearAgents()

    assert map.testNumberOfAgents() == 0
    assert map.tile(1).count() == 0
    assert map.tile(2).count() == 0
    assert map.tile(3).count() == 0