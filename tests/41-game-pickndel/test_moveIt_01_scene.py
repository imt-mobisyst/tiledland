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
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""

def test_pnd_mobile():
    mobile= pnd.Mobile()

def test_pnd_scene():
    model= pnd.Scene()
    model.initializeGrid( refMatrix, 0.9, 0.1 )
    artist= tll.Artist().initializePNG( "shot-test.png" )
    artist.fitBox( model.box(), 10 )

    artist.drawScene( model )
    artist.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-scene-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    bod= model.popBodyOn(1)
    print( bod )
    assert bod.id() == 1
    assert model.popBodyOn(25).id() == 2

    assert model.popBodyOn(7).id() == 3
    assert model.popBodyOn(44).id() == 4

    artist.drawScene( model )
    artist.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-scene-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_moveIt_neibors():
    # Game MoveIt:
    model= pnd.Scene()
    model.initializeGrid( refMatrix, 0.9, 0.1 )

    print( f">>> {model.neighbours(11)}" )

    assert model.neighbours(11) == [3, 11, 12, 18]
    assert model.directions(11) == [(0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (0.0, -1.0)]
    assert model.clockBearing(11) == [12, 0, 3, 6]
    assert model.completeClock(11) == [11,
                             11, 11, 12, 11, 11, 18,
                             11, 11, 11, 11, 11,  3 ]
    assert model.clockposition(11, 0) == 11
    assert model.clockposition(11, 12) == 3
    assert model.clockposition(11, 6) == 18
    assert model.clockposition(11, 3) == 12
    assert model.clockposition(11, 9) == 11

def test_moveIt_robots():
    # Game MoveIt:
    model= pnd.Scene( numberOfPlayers=2 )
    model.initializeGrid( refMatrix, 0.9, 0.1 )

    assert str(model.popRobot(1, 1)) == 'R-1: [1, 1, 0]'
    assert str(model.popRobot(1, 25)) == 'R-2: [1, 2, 0]'

    assert str(model.popRobot(2, 7)) == 'R-1: [2, 1, 0]'
    assert str(model.popRobot(2, 44)) == 'R-2: [2, 2, 0]'

    assert model.popRobot(3, 33) == False
    assert model.popRobot(1, 7) == False

    assert model.mobilePositions(1) == [1, 25]
    assert model.mobilePositions(2) == [7, 44]

    assert model.vips() == []

    assert model.move( 11, 12 ) == False
    assert model.move( 1, 6 ) == 10

    assert model.mobilePositions(1) == [10, 25]
    assert model.mobilePositions(2) == [7, 44]

    assert str( model.tile(10).piece() ) == 'R-1: [1, 1, 0]'

    assert model.clockBearing(44) == [9, 0, 3]

    assert model.move( 44, 12 ) == False
    assert model.move( 44, 3 ) == 45
    assert model.move( 45, 12 ) == 39
    assert model.move( 39,  0 ) == 39
    assert model.move( 39,  3 ) == False
    
    artist= tll.Artist().initializePNG( "shot-test.png" )
    artist.fitBox( model.box(), 10 )
    
    artist.drawMap( map )
    artist.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41-pickndel-scene-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )


    assert model.clockposition( 11, 12 ) == 3
    
"""
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""