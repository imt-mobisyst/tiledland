# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex
from src.tiledland import Entity, Tile, Tabletop 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_tabletop_hexaclock():
    tabletop= tll.Tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, 0, 0, 0, 0, -1, -1, -1]]  #
    )

    tll.draw( tabletop, "shot-test.png", 800, 600 )

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
    tabletop= tll.Tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, 0, 0, 0, 0, -1, -1, -1]], 1.4  #
    )

    for t in tabletop.tiles() :
        assert len( t.entities() ) == 0 
    
    tll.draw( tabletop, "shot-test.png", 800, 600 )
    
    tabletop.tileAppendEntity( 10, tll.Entity() )
    tll.draw( tabletop, "shot-test.png", 800, 600 )

    assert len( tabletop.tile(10).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 10 :
            assert len( t.entities() ) == 0 

    assert tabletop.tileClockMoveEntity(10, 1, 0) == 10
    tll.draw( tabletop, "shot-test.png", 800, 600 )

    assert len( tabletop.tile(10).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 10 :
            assert len( t.entities() ) == 0 

    assert tabletop.tileClockMoveEntity(10, 1, 3) == 11
    tll.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(11, 1, 7) == 17
    tll.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(17, 1, 2) == 17
    tll.draw( tabletop, "shot-test.png", 800, 600 )

    assert tabletop.tileClockMoveEntity(17, 1, 5) == 24
    tll.draw( tabletop, "shot-test.png", 800, 600 )
    
    assert len( tabletop.tile(24).entities() ) == 1
    for t in tabletop.tiles() :
        if t.index() != 24 :
            assert len( t.entities() ) == 0
    