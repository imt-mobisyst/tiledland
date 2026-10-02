import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point, Convex, Box
from src.tiledland import Entity, Mobile, Tile, Tabletop

# ----------------------------------------------------------------------- #
#           T E S T   T I L E D L A N D - I N T E G R A T E D   
# ----------------------------------------------------------------------- #

palette= [
    tild.Brush(0xffcd80, 0x603800, 4), # 0-Free
    tild.Brush(0xff6644, 0x991100, 4), # 1-Red
    tild.Brush(0x70f050, 0x20770a, 4), # 2-Green
    tild.Brush(0x6666ff, 0x1111aa, 4), # 3-Blue
    tild.Brush(0xfd9622, 0xdd550a, 4), # 4-Orange
    tild.Brush(0xdd77ff, 0x8800aa, 4), # 5-Purple
    tild.Brush(0x66ddee, 0x117799, 4), # 6-Cian
    tild.Brush(0xffffff, 0xbbbbbb, 4), # 7-White
    tild.Brush(0x888888, 0x555555, 4), # 8-Grey
    tild.Brush(0x444444, 0x000000, 4), # 9-Black

    tild.Brush(0x603800, 0xffcd80, 4), # 10-Background
    tild.Brush(0x991100, 0xff6644, 4), # 11-Red
    tild.Brush(0x20770a, 0x70f050, 4), # 12-Green
    tild.Brush(0x1111aa, 0x6666ff, 4), # 13-Blue
    tild.Brush(0xdd550a, 0xfd9622, 4), # 14-Orange
    tild.Brush(0x8800aa, 0xdd77ff, 4), # 15-Purple
    tild.Brush(0x117799, 0x66ddee, 4), # 16-Cian
    tild.Brush(0xbbbbbb, 0xffffff, 4), # 17-White
    tild.Brush(0x555555, 0x888888, 4), # 18-Grey
    tild.Brush(0x000000, 0x444444, 4)  # 19-Black
]

def draw(tabletop, filePath= "shot-test.png"):
    pablo= tild.artist.openPNG( filePath, 800, 600 )
    
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

    index= tabletop.appendTile( Tile( Convex() ) ).index()
    assert index == 1
    assert tabletop.size() == 1

    print( tabletop.tile(1) )
    assert tabletop.tile(1).position().asTuple() == (0.0, 0.0)
    assert tabletop.tile(1).shape().asZipped() == []

    index= tabletop.appendTile( Tile( Convex() ) ).index()
    assert index == 2
    assert tabletop.size() == 2

def test_tabletop_clockNeighboring():
    tabletop= Tabletop()
    tileConvex= Convex().fromZipped(
        [(-1.0, 0.0), (0.0, 1.5), (1.0, 0.0), (0.0, -1.5) ]
    )
    tabletop.appendTile( Tile(tileConvex).setBrush(palette[1]) )

    draw(tabletop)

    assert tabletop.neighbours(1) == []

    t= Tile(tileConvex)
    t.setPosition( Point(1.5, 2) )
    t.setBrush(palette[2])
    t= tabletop.appendTile(t)
    tabletop.connect( 1, t.index() )    
    assert tabletop.neighbours(1) == [(2, (1.5, 2.0), 1)]
    draw(tabletop)

    t= Tile(tileConvex)
    t.setPosition( Point(-1.5, 2) )
    t.setBrush(palette[2])
    t= tabletop.appendTile(t)

    tabletop.connect( 1, t.index() )

    tild.quickDraw(tabletop)

    print( tabletop.neighbours(1) )
    assert tabletop.neighbours(1) == [(2, (1.5, 2.0), 1), (3, (-1.5, 2.0), 11)]

    t= tabletop.appendTile( Tile( tileConvex, position=Point(1.5, -2) ).setBrush(palette[2]) )
    tabletop.connect( 1, t.index() )
    t= tabletop.appendTile( Tile( tileConvex, position=Point(-1.5, -2) ).setBrush(palette[2]) )
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
    assert tabletop.tile(1).shape().asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

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
    tabletop.tile(2).append( Mobile() )

    print( f">>>\n{tabletop}." )

    assert "\n"+str(tabletop)+"\n" == """
Tabletop:
- Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[1, 3] entities(0)
- Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[1, 2] entities(1)
  - Mobile 2-1 ⌊(-0.43, -0.5), (0.5, 0.5)⌉
- Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
"""

def test_Tabletop_hacka():
    tabletop= Tabletop().initLine(4, connect=False)
    tabletop.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    tabletop.tile(1).setCoordinates( 5.0, 3.0 )
    tabletop.tile(2).setCoordinates( 5.0, 15.0 )
    tabletop.tile(3).setCoordinates( 1.0, 9.0 )
    tabletop.tile(4).setCoordinates( 9.0, 9.0 )

    print(f">>>\n{tabletop}.")
    assert '\n'+ str(tabletop) +'\n' == """
Tabletop:
- Tile 0-1 ⌊(4.5, 2.5), (5.5, 3.5)⌉ adjs[2, 3, 4] entities(0)
- Tile 0-2 ⌊(4.5, 14.5), (5.5, 15.5)⌉ adjs[1, 3, 4] entities(0)
- Tile 0-3 ⌊(0.5, 8.5), (1.5, 9.5)⌉ adjs[1, 2] entities(0)
- Tile 0-4 ⌊(8.5, 8.5), (9.5, 9.5)⌉ adjs[1, 2] entities(0)
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

def test_Tabletop_connection():
    tabletop= Tabletop().initLine(3, connect=False)
    tabletop.connect(1, 2)
    tabletop.connect(2, 2)
    tabletop.connect(2, 3)
    tabletop.connect(3, 2)
    print( f">>>\n{tabletop}.")
    assert "\n"+ str(tabletop) +"\n" == """
Tabletop:
- Tile 0-1 ⌊(-0.5, -0.5), (0.5, 0.5)⌉ adjs[2] entities(0)
- Tile 0-2 ⌊(0.6, -0.5), (1.6, 0.5)⌉ adjs[2, 3] entities(0)
- Tile 0-3 ⌊(1.7, -0.5), (2.7, 0.5)⌉ adjs[2] entities(0)
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
- Tile 0-1 ⌊(0.53, 1.17), (1.4, 2.17)⌉ adjs[2, 3] entities(0)
- Tile 0-2 ⌊(0.05, 0.34), (0.92, 1.34)⌉ adjs[1, 3, 4] entities(0)
- Tile 0-3 ⌊(1.02, 0.34), (1.88, 1.34)⌉ adjs[1, 2] entities(0)
- Tile 0-4 ⌊(-0.43, -0.5), (0.43, 0.5)⌉ adjs[2] entities(0)"""