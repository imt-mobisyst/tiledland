import sys, hacka.py as hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

refMatrix= [
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
    [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
    [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
    [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
]
"""
      1   2   3       4   5   6   7   8   9
     10      11  12  13      14          15
     16  17  18      19  20  21      22  23
     24  25  26      27  28  29  30  31  32
     33      34  35  36      37            
     38      39      40  41  42            
     43  44  45  46  47      48            
"""

def test_gameengine_tools():
    game= mi.GameEngine( refMatrix, 2, 3, 1 )
    game.render()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    #print(game.asPod())

    gameCopy= mi.GameEngine().fromPod( game.asPod() )

    assert gameCopy.asPod() == game.asPod()

    print( gameCopy._map._mobiles )
    assert gameCopy._map._mobiles == [[48], [1,2,3], [4,5,6]]

    assert( game._map.tile(48)._pieces == game._map.tile(48)._pieces )
    assert( game._map.tile(48)._piecesBrushId == game._map.tile(48)._piecesBrushId )
    assert( game._map.tile(48)._piecesShapeId == game._map.tile(48)._piecesShapeId )

    assert( game._map.tile(1)._pieces == game._map.tile(1)._pieces )
    assert( game._map.tile(1)._piecesBrushId == game._map.tile(1)._piecesBrushId )
    assert( game._map.tile(1)._piecesShapeId == game._map.tile(1)._piecesShapeId )

    assert( game._map.tile(5)._pieces == game._map.tile(5)._pieces )
    assert( game._map.tile(5)._piecesBrushId == game._map.tile(5)._piecesBrushId )
    assert( game._map.tile(5)._piecesShapeId == game._map.tile(5)._piecesShapeId )

    gameCopy.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )
    
    gameCopy.setMoveAction(1, 1, 6)
    gameCopy.setMoveAction(2, 3, 3)
    gameCopy.setMoveAction(0, 1, 12)
    gameCopy.applyMoveActions()

    gameCopy.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
    
    game.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )


def test_gameengine_copy():
    model= mi.GameEngine( refMatrix, 2, 3, 1 )
    
    model.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    aCopy= model.copy()
    
    aCopy.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )
    
    aCopy.setMoveAction(1, 1, 6)
    aCopy.setMoveAction(2, 3, 3)
    aCopy.setMoveAction(0, 1, 12)
    aCopy.applyMoveActions()

    model.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    aCopy.render()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/06-simulate-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
    
    