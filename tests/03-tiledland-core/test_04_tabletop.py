# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Entity, Tile, Tabletop 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #
def draw( entity ):
    tll.draw( entity, "shot-test.png", 800, 600 )

def test_fast_tabletop_init():
    land= Tabletop()
    assert type(land) == Tabletop
    assert land.size() == 0
    assert land.box() == Box()

def test_fast_tabletop_initLine():
    tabletop= Tabletop().initLine(3, connect=False)
    assert tabletop.tile(1).index() == 1
    assert tabletop.tile(2).index() == 2
    assert tabletop.tile(3).index() == 3
    assert tabletop.tiles() == [ tabletop.tile(1), tabletop.tile(2), tabletop.tile(3) ]
    assert tabletop.edges() == []

    assert tabletop.tile(1).position().asTuple() == (0.0, 0.0)
    assert tabletop.tile(1).projectedShape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert tabletop.tile(2).position().asTuple() == (1.1, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in tabletop.tile(2).projectedShape().asZipped() ]
    assert env == [(0.6, -0.5), (0.6, 0.5), (1.6, 0.5), (1.6, -0.5)]

    assert tabletop.tile(3).position().asTuple() == (2.2, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in tabletop.tile(3).projectedShape().asZipped() ]
    assert env == [(1.7, -0.5), (1.7, 0.5), (2.7, 0.5), (2.7, -0.5)]
    
def test_fast_tabletop_construction():
    tabletop= Tabletop().initLine(3, connect=False)
    assert tabletop.tile(1).adjacencies() == []
    assert tabletop.tile(2).adjacencies() == []
    assert tabletop.tile(3).adjacencies() == []
    tabletop.connect(1, 2)
    tabletop.connect(1, 3)
    tabletop.connect(2, 2)
    tabletop.connect(2, 1)
    tabletop.connect(3, 1)
    tabletop.connect(3, 2)
    tabletop.connect(3, 3)
    assert tabletop.tile(1).adjacencies() == [2, 3]
    assert tabletop.tile(2).adjacencies() == [1, 2]
    assert tabletop.tile(3).adjacencies() == [1, 2, 3]
    assert tabletop.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idTabletop= id(tabletop)
    tabletop.initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {tabletop.edges()}")
    assert( idTabletop == id(tabletop) )
    assert tabletop.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_fast_tabletop_str():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    tabletop.tile(2).append( Entity(1) )

    print( f">>> {tabletop}." )

    assert "\n"+str(tabletop)+"\n" == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(1)
  - 1:Entity 2-1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

def test_fast_tabletop_hacka():
    tabletop= Tabletop().initLine(4, connect=False)
    tabletop.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    tabletop.tile(1).setPosition( 5.0, 3.0 )
    tabletop.tile(2).setPosition( 5.0, 15.0 )
    tabletop.tile(3).setPosition( 1.0, 9.0 )
    tabletop.tile(4).setPosition( 9.0, 9.0 )

    print(f">>>\n{tabletop}")
    assert '\n'+ str(tabletop) +'\n' == """
Tabletop:
- Tile-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] entities(0)
- Tile-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] entities(0)
- Tile-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] entities(0)
- Tile-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] entities(0)
"""

def test_fast_tabletop_box():
    tabletop= Tabletop()
    assert tabletop.box() == Box( [Point(0.0, 0.0)] )

    tabletop= Tabletop().initLine(4, connect=False)

    tll.draw( tabletop, "shot-test.svg", 800, 600 )
    print( tabletop.box() )
    assert str(tabletop.box()) == "⌊(-0.5, -0.5), (3.8, 0.5)⌉"
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-line-01.svg", "r").read())

    tabletop.initGrid( [[0, 1], [0, -1]] )

    tll.draw( tabletop, "shot-test.svg", 800, 600 )
    print( tabletop.box() )
    assert tabletop.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-grid-01.svg", "r").read())

def test_fast_tabletop_hacka():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    dt= tabletop.asDataTree()

    assert dt.label() == "Tabletop"

    assert dt.numberOfDigits() == 0
    assert dt.digits() == []
    
    assert dt.numberOfValues() == 1
    assert dt.values() == [0.01]
    
    assert dt.numberOfChildren() == 3
    assert dt.children() == [ t.asDataTree() for t in tabletop.tiles() ]

def test_fast_tabletop_DataTreecopy():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert tabletop.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    print( '>>>\n'+ str(tabletop) +'\n---')

    assert '\n'+ str(tabletop) +'\n' == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    print("Go for the copying...")
    tabletopBis= tabletop.dataTreeCopy()
    tabletop.connect(3, 1)

    assert type(tabletop) == type(tabletopBis)
    assert tabletopBis.size() == 3

    print(f">>>\n{tabletopBis}")
    assert '\n'+ str(tabletopBis) +'\n' == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert tabletopBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_fast_tabletop_connection():
    tabletop= Tabletop().initLine( 3, connect=False )
    tabletop.connect(1, 2)
    tabletop.connect(2, 2)
    tabletop.connect(2, 3)
    tabletop.connect(3, 2)
    print( f">>>\n{tabletop}\n---")
    assert "\n"+ str(tabletop) +"\n"  == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] entities(0)
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert tabletop.tile(1).adjacencies() == [2]
    assert tabletop.tile(2).adjacencies() == [2, 3]
    assert tabletop.tile(3).adjacencies() == [2]
    
    assert tabletop.isEdge(1, 2)
    assert tabletop.isEdge(2, 2)
    assert tabletop.isEdge(3, 2)
    assert not tabletop.isEdge(2, 1)
    assert not tabletop.isEdge(1, 3)
    assert not tabletop.isEdge(3, 1)
  
def test_fast_tabletop_withEntities():
    tabletop= Tabletop().initGrid( [[0, 1],[-1, 0]] )
    
    assert tabletop.numberOfEntities() == 0
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 0
    assert tabletop.tile(3).numberOfEntities() == 0
    
    tabletop.tileAppendEntity(2)

    assert tabletop.numberOfEntities() == 1
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 1
    assert tabletop.tile(3).numberOfEntities() == 0

    tabletop.tileAppendEntity(1)

    assert tabletop.numberOfEntities() == 2
    assert tabletop.tile(1).numberOfEntities() == 1
    assert tabletop.tile(2).numberOfEntities() == 1
    assert tabletop.tile(3).numberOfEntities() == 0

    bod= tabletop.tileAppendEntity(2)

    assert tabletop.numberOfEntities() == 3
    assert tabletop.tile(1).numberOfEntities() == 1
    assert tabletop.tile(2).numberOfEntities() == 2
    assert tabletop.tile(3).numberOfEntities() == 0

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] entities(1)
  - 0:Entity 1-1 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- 1:Tile 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] entities(2)
  - 0:Entity 2-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - 0:Entity 2-2 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- 0:Tile 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] entities(0)"""

    tabletop.clearEntities()

    assert tabletop.numberOfEntities() == 0
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 0
    assert tabletop.tile(3).numberOfEntities() == 0

def test_fast_tabletop_popEntities():
    tabletop= Tabletop().initGrid( [[0, 1],[-1, 0]] )
    
    assert tabletop.numberOfEntities() == 0
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 0
    assert tabletop.tile(3).numberOfEntities() == 0
    
    bod= tabletop.tileAppendEntity(2)

    assert type(bod) == Entity
    assert bod.location() == (2, 1)
    assert tabletop.entity(2, 1) == bod

    assert tabletop.numberOfEntities() == 1
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 1
    assert tabletop.tile(3).numberOfEntities() == 0

    bod= tabletop.tileAppendEntity(1)

    assert type(bod) == Entity
    assert bod.location() == (1, 1)
    assert tabletop.entity(1, 1) == bod

    bod= tabletop.tileAppendEntity(1)

    assert type(bod) == Entity
    assert bod.location() == (1, 2)
    assert tabletop.entity(1, 1) != bod
    assert tabletop.entity(1, 2) == bod

    assert tabletop.numberOfEntities() == 3
    assert tabletop.tile(1).numberOfEntities() == 2
    assert tabletop.tile(2).numberOfEntities() == 1
    assert tabletop.tile(3).numberOfEntities() == 0

    bod= tabletop.tileAppendEntity(2)

    assert tabletop.numberOfEntities() == 4
    assert tabletop.tile(1).numberOfEntities() == 2
    assert tabletop.tile(2).numberOfEntities() == 2
    assert tabletop.tile(3).numberOfEntities() == 0

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] entities(2)
  - 0:Entity 1-1 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
  - 0:Entity 1-2 ⌊(-0.43, 0.6), (0.5, 1.6)⌉
- 1:Tile 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] entities(2)
  - 0:Entity 2-1 ⌊(0.67, 0.6), (1.6, 1.6)⌉
  - 0:Entity 2-2 ⌊(0.67, 0.6), (1.6, 1.6)⌉
- 0:Tile 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] entities(0)"""

    tabletop.clearEntities()

    assert tabletop.numberOfEntities() == 0
    assert tabletop.tile(1).numberOfEntities() == 0
    assert tabletop.tile(2).numberOfEntities() == 0
    assert tabletop.tile(3).numberOfEntities() == 0

def test_fast_tabletop_moveEntities():
    tabletop= Tabletop().initGrid( [[0, 0, 1],[-1, 0, 0], [2, 0, -1]] )
    draw(tabletop)

    c= 1
    entShape= Convex().initArrowTip(0.4)
    for i in [1, 1, 2, 2, 3] :
        tabletop.tileAppendEntity(i, Entity(shape=entShape, name= f"E.{c}")  )
        c+= 1

    draw(tabletop)
    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - 0:E.1 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.2 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- 0:Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(2)
  - 0:E.3 2-1 ⌊(0.93, 2.0), (1.3, 2.4)⌉
  - 0:E.4 2-2 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- 1:Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - 0:E.5 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- 0:Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- 0:Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- 2:Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- 0:Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= tabletop.tileRemoveEntity(2, 1)

    print( bob )
    assert str(bob) == "0:E.3 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - 0:E.1 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.2 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- 0:Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(1)
  - 0:E.4 2-1 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- 1:Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - 0:E.5 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- 0:Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- 0:Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- 2:Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- 0:Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""
    
    bob= tabletop.tileRemoveEntity(2, 1)

    print( bob )
    assert str(bob) == "0:E.4 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - 0:E.1 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.2 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- 0:Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- 1:Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(1)
  - 0:E.5 3-1 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- 0:Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- 0:Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- 2:Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- 0:Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= tabletop.moveEntity(3, 1, 1)

    print( bob )
    assert bob.name() == "E.5"
    assert bob.location() == (1, 3)

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(3)
  - 0:E.1 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.2 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.5 1-3 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- 0:Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- 1:Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(0)
- 0:Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(0)
- 0:Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- 2:Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- 0:Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""

    bob= tabletop.moveEntity(1, 2, 4)

    print( bob )
    assert bob.name() == "E.2"
    assert bob.location() == (4, 1)

    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] entities(2)
  - 0:E.1 1-1 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - 0:E.5 1-2 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- 0:Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] entities(0)
- 1:Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] entities(0)
- 0:Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] entities(1)
  - 0:E.2 4-1 ⌊(0.93, 0.9), (1.3, 1.3)⌉
- 0:Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] entities(0)
- 2:Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] entities(0)
- 0:Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] entities(0)"""
