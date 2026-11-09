# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tild
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Unit, Tile, Map

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #
def test_fast_map_init():
    m= Map()
    assert type(m) == Map
    assert m.size() == 0
    assert m.box() == Box()

def test_fast_map_initLine():
    m= Map().initLine(3, connect=False)
    assert m.tile(1).index() == 1
    assert m.tile(2).index() == 2
    assert m.tile(3).index() == 3
    assert m.tiles() == [ m.tile(1), m.tile(2), m.tile(3) ]
    assert m.edges() == []

    assert m.tile(1).position().asTuple() == (0.0, 0.0)
    assert m.tile(1).shape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert m.tile(2).position().asTuple() == (1.1, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in m.tile(2).shape().asZipped() ]
    assert env == [(0.6, -0.5), (0.6, 0.5), (1.6, 0.5), (1.6, -0.5)]

    assert m.tile(3).position().asTuple() == (2.2, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in m.tile(3).shape().asZipped() ]
    assert env == [(1.7, -0.5), (1.7, 0.5), (2.7, 0.5), (2.7, -0.5)]
    
def test_fast_map_construction():
    m= Map().initLine(3, connect=False)
    assert m.tile(1).adjacencies() == []
    assert m.tile(2).adjacencies() == []
    assert m.tile(3).adjacencies() == []
    m.connect(1, 2)
    m.connect(1, 3)
    m.connect(2, 2)
    m.connect(2, 1)
    m.connect(3, 1)
    m.connect(3, 2)
    m.connect(3, 3)
    assert m.tile(1).adjacencies() == [2, 3]
    assert m.tile(2).adjacencies() == [1, 2]
    assert m.tile(3).adjacencies() == [1, 2, 3]
    assert m.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idMap= id(m)
    m.initLine(3, connect=False)
    m.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {m.edges()}")
    assert( idMap == id(m) )
    assert m.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_fast_map_str():
    m= Map().initLine(3, connect=False)
    m.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    m.tile(2).append( Unit().setIdentity(1, 1) )

    print( f">>> {m}." )

    assert "\n"+str(m)+"\n" == """
Map:
- Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] units(0)
- Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] units(1)
  - Unit 1-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉
- Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] units(0)
"""

def test_fast_map_hacka():
    m= Map().initLine(4, connect=False)
    m.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    m.tile(1).setPosition( Point(5.0, 3.0) )
    m.tile(2).setPosition( Point(5.0, 15.0) )
    m.tile(3).setPosition( Point(1.0, 9.0) )
    m.tile(4).setPosition( Point(9.0, 9.0) )

    print(f">>>\n{m}")
    assert '\n'+ str(m) +'\n' == """
Map:
- Tile 0-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] units(0)
- Tile 0-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] units(0)
- Tile 0-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] units(0)
- Tile 0-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] units(0)
"""

def test_fast_map_box():
    m= Map()
    assert m.box() == Box( [Point(0.0, 0.0)] )

    m= Map().initLine(4, connect=False)

    tild.drawMap( m, "shot-test.png", 800, 600 )
    tild.drawMap( m, "shot-test.svg", 800, 600 )

    print( m.box() )
    assert str(m.box()) == "⌊(-0.5, -0.5), (3.8, 0.5)⌉"
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-line-01.svg", "r").read())

    m.initGrid( [[0, 1], [0, -1]] )

    assert m.size() == 3
    assert m.tile(1).category() == 0
    assert m.tile(2).category() == 1
    assert m.tile(3).category() == 0

    tild.drawMap( m, "shot-test.png", 800, 600 )
    tild.drawMap( m, "shot-test.svg", 800, 600 )
    print( m.box() )
    assert m.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]
    assert ( open("shot-test.svg", "r").read()
        == open("tests/refs/03.04-map-grid-01.svg", "r").read())

def test_fast_map_connection():
    m= Map().initLine( 3, connect=False )
    m.connect(1, 2)
    m.connect(2, 2)
    m.connect(2, 3)
    m.connect(3, 2)
    print( f">>>\n{m}\n---")

    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert "\n"+ str(m) +"\n"  == """
Map:
- Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] units(0)
- Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] units(0)
- Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] units(0)
"""

    assert m.tile(1).adjacencies() == [2]
    assert m.tile(2).adjacencies() == [2, 3]
    assert m.tile(3).adjacencies() == [2]
    
    assert m.isEdge(1, 2)
    assert m.isEdge(2, 2)
    assert m.isEdge(3, 2)
    assert not m.isEdge(2, 1)
    assert not m.isEdge(1, 3)
    assert not m.isEdge(3, 1)
  
def test_fast_map_withUnits():
    m= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert m.numberOfUnits() == 0
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 0
    assert m.tile(3).numberOfUnits() == 0
    
    m.tile(2).appendCenter(Unit(index=1))

    assert m.numberOfUnits() == 1
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 1
    assert m.tile(3).numberOfUnits() == 0

    m.tile(1).appendCenter(Unit(index=2))

    assert m.numberOfUnits() == 2
    assert m.tile(1).numberOfUnits() == 1
    assert m.tile(2).numberOfUnits() == 1
    assert m.tile(3).numberOfUnits() == 0

    bod= m.tile(2).appendCenter(Unit(index=3))

    assert m.numberOfUnits() == 3
    assert m.tile(1).numberOfUnits() == 1
    assert m.tile(2).numberOfUnits() == 2
    assert m.tile(3).numberOfUnits() == 0

    tild.drawMap( m, "shot-test.png", 800, 600 )
    print( f"---\n{m}.")
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] units(1)
  - Unit 0-2 ⌊(-0.5, 0.6), (0.5, 1.6)⌉
- Tile 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] units(2)
  - Unit 0-1 ⌊(0.6, 0.6), (1.6, 1.6)⌉
  - Unit 0-3 ⌊(0.6, 0.6), (1.6, 1.6)⌉
- Tile 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] units(0)"""

    m.clearUnits()

    assert m.numberOfUnits() == 0
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 0
    assert m.tile(3).numberOfUnits() == 0

def test_fast_map_popUnits():
    m= Map().initGrid( [[0, 1],[-1, 0]] )
    
    assert m.numberOfUnits() == 0
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 0
    assert m.tile(3).numberOfUnits() == 0

    bod= Unit(index=1)
    i= m.tile(2).appendCenter(bod)

    assert type(bod) == Unit
    assert i == 1
    assert m.unit(2, 1) == bod

    assert m.numberOfUnits() == 1
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 1
    assert m.tile(3).numberOfUnits() == 0

    bod= Unit(index=2)
    i= m.tile(1).appendCenter(bod)

    assert type(bod) == Unit
    assert i == 1
    assert m.unit(1, 1) == bod


    bod= Unit(index=3)
    i= m.tile(1).appendCenter(bod)

    assert type(bod) == Unit
    assert i == 2
    assert m.unit(1, 1) != bod
    assert m.unit(1, 2) == bod

    assert m.numberOfUnits() == 3
    assert m.tile(1).numberOfUnits() == 2
    assert m.tile(2).numberOfUnits() == 1
    assert m.tile(3).numberOfUnits() == 0

    m.tile(2).appendCenter(Unit(index=4))

    assert m.numberOfUnits() == 4
    assert m.tile(1).numberOfUnits() == 2
    assert m.tile(2).numberOfUnits() == 2
    assert m.tile(3).numberOfUnits() == 0

    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 0.6), (0.5, 1.6)⌉ adjs[2] units(2)
  - Unit 0-2 ⌊(-0.5, 0.6), (0.5, 1.6)⌉
  - Unit 0-3 ⌊(-0.5, 0.6), (0.5, 1.6)⌉
- Tile 0-2 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[1, 3] units(2)
  - Unit 0-1 ⌊(0.6, 0.6), (1.6, 1.6)⌉
  - Unit 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉
- Tile 0-3 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2] units(0)"""

    m.clearUnits()

    assert m.numberOfUnits() == 0
    assert m.tile(1).numberOfUnits() == 0
    assert m.tile(2).numberOfUnits() == 0
    assert m.tile(3).numberOfUnits() == 0

def test_fast_map_moveUnits():
    m= Map().initGrid( [[0, 0, 1],[-1, 0, 0], [2, 0, -1]] )
    tild.drawMap( m, "shot-test.png", 800, 600 )
    
    c= 1
    entShape= Convex().initArrowTip(0.4)
    for i in [1, 1, 2, 2, 3] :
        m.tile(i).appendCenter( Unit(entShape).setName(f"M.{c}") )
        c+= 1

    tild.drawMap( m, "shot-test.png", 800, 600 )
    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] units(2)
  - M.1 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.2 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] units(2)
  - M.3 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉
  - M.4 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] units(1)
  - M.5 0-0 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] units(0)
- Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] units(0)
- Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] units(0)
- Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] units(0)"""

    bob= m.tileRemoveUnit(2, 1)

    print( bob )
    assert str(bob) == "M.3 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] units(2)
  - M.1 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.2 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] units(1)
  - M.4 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉
- Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] units(1)
  - M.5 0-0 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] units(0)
- Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] units(0)
- Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] units(0)
- Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] units(0)"""
    
    bob= m.tileRemoveUnit(2, 1)

    print( bob )
    assert str(bob) == "M.4 0-0 ⌊(0.93, 2.0), (1.3, 2.4)⌉"

    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] units(2)
  - M.1 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.2 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] units(0)
- Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] units(1)
  - M.5 0-0 ⌊(2.03, 2.0), (2.4, 2.4)⌉
- Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] units(0)
- Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] units(0)
- Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] units(0)
- Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] units(0)"""

    i= m.tileMoveUnit(3, 1, 1)
    assert i == 3
    bob= m.unit(1, i)

    print( bob )
    assert bob.name() == "M.5"

    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] units(3)
  - M.1 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.2 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.5 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] units(0)
- Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] units(0)
- Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] units(0)
- Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] units(0)
- Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] units(0)
- Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] units(0)"""

    i= m.tileMoveUnit(1, 2, 4)
    assert i == 1
    bob= m.unit(4, i)

    print( bob )
    assert bob.name() == "M.2"

    print( f"---\n{m}.")
    tild.drawMap( m, "shot-test.png", 800, 600 )
    assert str(m) == """Map:
- Tile 0-1 ⌊(-0.5, 1.7), (0.5, 2.7)⌉ adjs[2] units(2)
  - M.1 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
  - M.5 0-0 ⌊(-0.17, 2.0), (0.2, 2.4)⌉
- Tile 0-2 ⌊(0.6, 1.7), (1.6, 2.7)⌉ adjs[1, 3, 4] units(0)
- Tile 0-3 ⌊(1.7, 1.7), (2.7, 2.7)⌉ adjs[2, 5] units(0)
- Tile 0-4 ⌊(0.6, 0.6), (1.6, 1.6)⌉ adjs[2, 5, 7] units(1)
  - M.2 0-0 ⌊(0.93, 0.9), (1.3, 1.3)⌉
- Tile 0-5 ⌊(1.7, 0.6), (2.7, 1.6)⌉ adjs[3, 4] units(0)
- Tile 0-6 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[7] units(0)
- Tile 0-7 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[4, 6] units(0)"""
