# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tild
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Entity, Tile, Tabletop 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_tabletop_clock():
    clockAngle= [ round(x, 4) for x in tild.CLOCK_ANGLES ]
    print( clockAngle )
    assert len(tild.tabletop.CLOCK_ANGLES) == 13
    assert clockAngle == [1.5708, 1.0472, 0.5236, 0.0, -0.5236, -1.0472, -1.5708, -2.0944, -2.618, 3.1416, 2.618, 2.0944, 1.5708]

    tabletop= tild.Tabletop().initHexa(
        [[-1, 0, 0], 
        [0, 0, 0], 
        [-1, 0, 0]] 
    )
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    bob= tild.Entity()
    tabletop.tileAppendEntity( 4, bob )
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert round( bob.orientation(), 4) == 0.0

    tabletop.tileOrientEntity(4, 1, 1.2)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == 1.2

    tabletop.tileRotateEntity(4, 1, 0.8)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == 2.0

    tabletop.tileClockOrientEntity(4, 1, 7)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == -2.0944

    tabletop.tileRotateEntityLeft(4, 1)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == -1.5708
    
    tabletop.tileRotateEntityRight(4, 1)
    tabletop.tileRotateEntityRight(4, 1)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == -2.618

    tabletop.tileRotateEntityRight(4, 1)
    tabletop.tileRotateEntityRight(4, 1)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == 2.618
    
    tabletop.tileOrientEntity(4, 1, 387.2)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == -2.3575

    tabletop.tileOrientEntity(4, 1, -55.2)
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 4) == 1.3487

def test_fast_tabletop_hexaclock():
    tabletop= tild.Tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, 0, 0, 0, 0, -1, -1, -1]]  #
    )

    tild.draw( tabletop, "shot-test.png", 800, 600 )

    neibors= tabletop.neighbours(22)
    print( neibors )
    assert( [ (iTile, clock) for iTile, pos, clock in neibors ]
        == [(15, 11), (16, 1), (21, 9), (23, 3), (28, 7), (29, 5)] )
    assert( [ (round(x, 2), round(y, 2)) for x, y in tabletop.directions(22) ]
        == [(-0.48, 0.84), (0.48, 0.84), (-0.97, 0.0), (0.97, 0.0), (-0.48, -0.84), (0.48, -0.84)] )
        
    assert( tabletop.completeClock(22)  == [22,  16, 22, 23,  22, 29, 22,  28, 22, 21,  22, 15, 22] )


    neibors= tabletop.neighbours(9)
    print( neibors )
    assert( [ (iTile, clock) for iTile, pos, clock in neibors ]
        == [(3, 11), (10, 3), (16, 7)] )
    assert( tabletop.completeClock(9)  == [9,  9, 9, 10,  9, 9, 9,  16, 9, 9,  9, 3, 9] )

    neibors= tabletop.neighbours(27)
    print( neibors )
    assert( [ (iTile, clock) for iTile, pos, clock in neibors ]
        == [(20, 11), (26, 9)] )

    assert( tabletop.completeClock(27)  == [27,  27, 27, 27,  27, 27, 27,  27, 27, 26,  27, 20, 27] )

def test_fast_tabletop_hexamove():
    tabletop= tild.Tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, 0, 0, 0, 0, -1, -1, -1]], 1.4  #
    )

    for t in tabletop.tiles() :
        assert len( t.entities() ) == 0 
    
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    
    tabletop.tileAppendEntity( 10, tild.Entity() )
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert len( tabletop.tile(10).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 10 :
            assert len( t.entities() ) == 0 

    assert tabletop.tileClockMoveEntity(10, 1, 0) == 10
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert len( tabletop.tile(10).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 10 :
            assert len( t.entities() ) == 0 

    assert tabletop.tileClockMoveEntity(10, 1, 3) == 11
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(11, 1, 7) == 17
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(17, 1, 2) == 17
    tild.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(17, 1, 5) == 24
    tild.draw( tabletop, "shot-test.png", 800, 600 )
    
    assert len( tabletop.tile(24).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 24 :
            assert len( t.entities() ) == 0
    