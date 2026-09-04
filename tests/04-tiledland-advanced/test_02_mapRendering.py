import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point, Convex, Box
from src.tiledland import Entity, Tile, Tabletop

# ----------------------------------------------------------------------- #
#           T E S T   T I L E D L A N D - I N T E G R A T E D   
# ----------------------------------------------------------------------- #

def draw(tabletop, filePath= "shot-test.png"):
    pablo= tild.createArtistPNG( filePath, 800, 600 )
    
    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    tabletop.renderNetworkOn(pablo)
    tabletop.renderTilesOn(pablo)

    pablo.flip()

def test_tabletop_incremental():
    tabletop= Tabletop()
    
    assert type(tabletop) == Tabletop
    assert tabletop.size() == 0
    assert tabletop.box() == Box()

    index= tabletop.appendTile( Tile( shape= Convex() ) ).index()
    assert index == 1
    assert tabletop.size() == 1

    print( tabletop.tile(1) )
    assert tabletop.tile(1).position().asTuple() == (0.0, 0.0)
    assert tabletop.tile(1).projectedShape().asZipped() == []

    index= tabletop.appendTile( Tile( shape= Convex() ) ).index()
    assert index == 2
    assert tabletop.size() == 2

def test_tabletop_clockNeighboring():
    tabletop= Tabletop()
    tileConvex= Convex().fromZipped(
        [(-1.0, 0.0), (0.0, 1.5), (1.0, 0.0), (0.0, -1.5) ]
    )
    tabletop.appendTile( Tile( shape=tileConvex, group= 1 ) )

    draw(tabletop)

    assert tabletop.neighbours(1) == []

    t= tabletop.appendTile( Tile( shape= tileConvex, position=Point(1.5, 2), group= 2 ) )
    tabletop.connect( 1, t.index() )    
    assert tabletop.neighbours(1) == [(2, (1.5, 2.0), 1)]
    draw(tabletop)

    t= tabletop.appendTile( Tile( shape= tileConvex, position=Point(-1.5, 2), group= 2 ) )
    tabletop.connect( 1, t.index() )    
    draw(tabletop)

    print( tabletop.neighbours(1) )
    assert tabletop.neighbours(1) == [(2, (1.5, 2.0), 1), (3, (-1.5, 2.0), 11)]

    t= tabletop.appendTile( Tile( shape= tileConvex, position=Point(1.5, -2), group= 2 ) )
    tabletop.connect( 1, t.index() )    
    t= tabletop.appendTile( Tile( shape= tileConvex, position=Point(-1.5, -2), group= 2 ) )
    tabletop.connect( 1, t.index() )    
    draw(tabletop)

    print( tabletop.neighbours(1) )
    assert tabletop.neighbours(1) == [(2, (1.5, 2.0), 1), (3, (-1.5, 2.0), 11), (4, (1.5, -2.0), 5), (5, (-1.5, -2.0), 7)]

    assert tabletop.tile(1).adjacencies() == [2, 3, 4, 5]
    assert tabletop.edges() == [(1, 2), (1, 3), (1, 4), (1, 5)]

def test_Tabletop_initLine():
    tabletop= Tabletop().initLine(3, connect=False)
    assert tabletop.tile(1).index() == 1
    assert tabletop.tile(2).index() == 2
    assert tabletop.tile(3).index() == 3
    assert tabletop.tiles() == [ tabletop.tile(1), tabletop.tile(2), tabletop.tile(3) ]
    assert tabletop.edges() == []

    assert tabletop.tile(1).position().asTuple() == (0.0, 0.0)
    assert tabletop.tile(1).projectedShape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    assert tabletop.tile(2).position().asTuple() == (1.1, 0.0)
    assert tabletop.tile(3).position().asTuple() == (2.2, 0.0)
    
def test_Tabletop_construction():
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

def test_Tabletop_str():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    tabletop.tile(2).append( Entity(1) )

    print( f">>>\n{tabletop}." )

    assert "\n"+str(tabletop)+"\n" == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(1)
  - 1:Entity 2-1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

def test_Tabletop_hacka():
    tabletop= Tabletop().initLine(4, connect=False)
    tabletop.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    tabletop.tile(1).setPosition( 5.0, 3.0 )
    tabletop.tile(2).setPosition( 5.0, 15.0 )
    tabletop.tile(3).setPosition( 1.0, 9.0 )
    tabletop.tile(4).setPosition( 9.0, 9.0 )

    print(f">>>\n{tabletop}.")
    assert '\n'+ str(tabletop) +'\n' == """
Tabletop:
- 0:Tile 0-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] entities(0)
- 0:Tile 0-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] entities(0)
- 0:Tile 0-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] entities(0)
- 0:Tile 0-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] entities(0)
"""

def test_Tabletop_box():
    tabletop= Tabletop()
    assert tabletop.box() == Box( [Point(0.0, 0.0)] )

    tabletop= Tabletop().initLine(4, connect=False)
    box= tabletop.box()
    print(box)
    box.round(3)
    assert box.asZip() == [(-0.5, -0.5), (3.8, 0.5)]
    
    tabletop.initGrid( [[0, 1], [0, -1]] )
    print( tabletop.box() )
    assert tabletop.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]

def test_Tabletop_hacka2():
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

def test_Tabletop_dataTreecopy():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert tabletop.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]
    print( f">>>\n{tabletop}." )
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

    print(f">>>\n{tabletopBis}.")
    assert '\n'+ str(tabletopBis) +'\n' == """
Tabletop:
- 0:Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- 0:Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(0)
- 0:Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

    assert tabletopBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_Tabletop_connection():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connect(1, 2)
    tabletop.connect(2, 2)
    tabletop.connect(2, 3)
    tabletop.connect(3, 2)
    print( f">>>\n{tabletop}.")
    assert "\n"+ str(tabletop) +"\n" == """
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

def test_Tabletop_hexa():
    tabletop= Tabletop().initHexa(
        [[-1, 0],
           [1, 0],
         [0, -1]]
    )
    draw(tabletop)
    print( f"---\n{tabletop}.")
    assert str(tabletop) == """Tabletop:
- 0:Tile 0-1 ⌊(0.53, 1.17), (1.4, 2.17)⌉ adjs[2, 3] entities(0)
- 1:Tile 0-2 ⌊(0.05, 0.34), (0.92, 1.34)⌉ adjs[1, 3, 4] entities(0)
- 0:Tile 0-3 ⌊(1.02, 0.34), (1.88, 1.34)⌉ adjs[1, 2] entities(0)
- 0:Tile 0-4 ⌊(-0.43, -0.5), (0.43, 0.5)⌉ adjs[2] entities(0)"""