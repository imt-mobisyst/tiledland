import sys, hacka.py as hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_gamemaster_method():
    game= mi.GameEngine( missions=[(1, 2)], tic=20)
    master= mi.GameMaster( game )

    assert( type( master.initialize().asPod() ) is hacka.Pod  )
    assert( type( master.playerHand(1).asPod() ) is hacka.Pod )
    assert( master.applyPlayerAction( 1, "move 1 0" )  )
    
    master.tic()
    assert( not master.isEnded() )
    
    assert( master.playerScore(1) == 19.0 )

    master.tic()
    assert( not master.isEnded() )
    
    assert( master.playerScore(1) == 18.0 )

def test_gamemaster_live_cycle():
    game= mi.GameEngine( tic= 10, missions=[(1, 2)] )
    master= mi.GameMaster( game )

    assert master.initialize()

    t= 10
    while t > 0 :
        assert not master.isEnded()
        assert game.tic() == t
        master.tic()
        t-= 1

    assert( master.isEnded() )
    
def test_gamemaster_moves():
    game= mi.GameEngine( tic= 10, missions= [(4, 5), (7, 8)] )
    master= mi.GameMaster( game )

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-04.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game._map.mobilePositions(1) == [1]

    # Turn 1
    master.initialize()
    master.playerHand(1)
    master.applyPlayerAction( 1, "move 1 6" )
    master.tic()

    assert game.mobilePosition(1, 1) == 4
    assert game.mobileMission(1, 1) == 0
    
    # Turn 2
    master.playerHand(1)
    master.applyPlayerAction( 1, "mission 1 1" )
    master.tic()

    assert game.mobilePosition(1, 1) == 4
    assert game.mobileMission(1, 1) == 1
    
    # Turn 3-6
    moves= [12, 3, 3, 6]
    for m in moves :
        master.playerHand(1)
        master.applyPlayerAction( 1, f"move 1 {m}" )
        master.tic()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobileMission(1, 1) == 1
    assert game.score(1) == 0.0

    # Turn 7
    master.playerHand(1)
    master.applyPlayerAction( 1, "mission 1 1 move 1 12" )
    master.tic()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobileMission(1, 1) == 0
    assert game.score(1) == 10.0

def test_gamemaster_distances_path():
    game= mi.GameEngine(
        matrix= [
            [00, 00, 00, 00],
            [-1, 00, -1, -1],
            [00, 00, 00, 00],
            [00, -1, -1, 00]
        ],
        tic= 10, missions= [(4, 5), (7, 8)] )
    master= mi.GameMaster( game )

    assert master.mapSize() == 11
    assert master._distances == [
        [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        [ 1, 0, 1, 2, 3, 2, 4, 3, 4, 5,  5,  6],
        [ 2, 1, 0, 1, 2, 1, 3, 2, 3, 4,  4,  5],
        [ 3, 2, 1, 0, 1, 2, 4, 3, 4, 5,  5,  6],
        [ 4, 3, 2, 1, 0, 3, 5, 4, 5, 6,  6,  7],
        [ 5, 2, 1, 2, 3, 0, 2, 1, 2, 3,  3,  4],
        [ 6, 4, 3, 4, 5, 2, 0, 1, 2, 3,  1,  4],
        [ 7, 3, 2, 3, 4, 1, 1, 0, 1, 2,  2,  3],
        [ 8, 4, 3, 4, 5, 2, 2, 1, 0, 1,  3,  2],
        [ 9, 5, 4, 5, 6, 3, 3, 2, 1, 0,  4,  1],
        [10, 5, 4, 5, 6, 3, 1, 2, 3, 4,  0,  5],
        [11, 6, 5, 6, 7, 4, 4, 3, 2, 1,  5,  0]
    ]

    assert master.toward(1, 2) == (3, 2)
    assert master.toward(4, 4) == (0, 4)
    assert master.toward(5, 11) == (6, 7)

    assert master.path(1, 11) == (
        [3, 6, 6, 3, 3, 6],
        [2, 5, 7, 8, 9, 11]
    )

def test_gamemaster_options():
    game= mi.GameEngine(
        matrix= [
            [00, 00, 00, 00],
            [-1, 00, 00, -1],
            [00, 00, 00, 00],
            [00, -1, -1, 00]
        ],
        tic= 10, missions= [(4, 5), (7, 8)] )
    master= mi.GameMaster( game )

    assert master.moveOptions(1, 2) == [(3, 2)]
    assert master.moveOptions(4, 4) == [(0, 4)]
    assert master.moveOptions(5, 11) == [(6, 8)]
    assert master.moveOptions(5, 12) == [(3, 6), (6, 8)]


def test_gamemaster_loops():
    game= mi.GameEngine(
        matrix= [
            [00, 00, 00, 00],
            [-1, 00, -1, -1],
            [00, 00, 00, 00],
            [00, -1, -1, 00]
        ],
        tic= 10 )
    master= mi.GameMaster( game, randomMission=4 )

    assert master._engine._map._mobiles == [[], [1]]
    assert master._engine._missions  == []

    master.initialize()
    assert len( master._engine._missions ) == 4
    assert master._engine._tic == 10

    master._engine.setMoveAction(1, 1, 3)
    master._engine.applyMoveActions()

    assert master._engine._tic == 9
    assert master._engine._map._mobiles == [[], [2]]

    master._engine.setMoveAction(1, 1, 6)
    master._engine.applyMoveActions()

    assert master._engine._tic == 8
    assert master._engine._map._mobiles == [[], [5]]

    assert master.playerScore(1) == 8.0
    
    master._engine._scores= [0, 100.0]
    assert master.playerScore(1) == 108.0

    master.initialize()

    assert master._engine._tic == 10
    assert master._engine._map._mobiles == [[], [5]]
    assert master.playerScore(1) == 10.0