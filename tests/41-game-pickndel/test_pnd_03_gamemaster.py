import sys, hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_gamemaster_method():
    world= pnd.World().initializeGrid( [[0, 0], [0, 0]] )
    game= pnd.GameEngine( world, 1, tic=20 )

    assert( len(game._model._agents) == 2 )

    print( f">>> {type( game.initialize() )} is {hacka.Pod}")

    assert( type( game.initialize() ) is hacka.Pod )
    assert( type( game.playerHand(1) ) is hacka.Pod )
    assert( game.applyAction( "go 0", 1 )  )
    assert( game.applyAction( "do 1", 1 )  )
    
    game.tic()
    assert( not game.isEnded() )
    assert( game.playerScore(1) == 0.0 )

    game.tic()
    assert( not game.isEnded() )
    assert( game.playerScore(1) == 0.0 )

    world.setMissions( [] )
    assert len( world.missions() ) == 0

    world.setMissions( [(1, 2)] )
    assert len( world.missions() ) == 1
    assert world.mission(1).asTuple() == (1, 2, 124, 0)

def test_gamemaster_live_cycle():
    world= pnd.World()
    world.initializeGrid( [[0, 0], [0, 0]] )
    game= pnd.GameEngine( world, 1, tic=10 )

    assert game.initialize()
    world.setMissions( [(1, 2)] )

    t= 10
    while t > 0 :
        assert not game.isEnded()
        assert game.ticCounter() == t
        game.tic()
        t-= 1

    assert len( world.missions() ) == 1
    assert world.mission(1).asTuple() == (1, 2, 124, 0)
    assert( game.isEnded() )
    
def test_gamemaster_moves():
    world= pnd.World()
    world.initializeGrid( [[0, 0, 0, -1], [0, -1, 0, 0], [0, 0, 0, 0]] )
    game= pnd.GameEngine( world, 1, tic=20 )
    world.teleport( world.agent(1, 1,).tile(), 1 )
    game.initialize()
    world.setMissions( [(4, 5), (7, 8)] )

    world.render()

    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert world.carrierTiles(1) == [1]

    # Turn 1
    game.playerHand(1)
    game.applyAction( "go 6", 1 )

    assert str(world.agent(1, 1)) == "Carrier-1.1 ⌊(-0.18, 2.02), (0.18, 2.38)⌉ |6, 0|"

    game.tic()
    assert world.agent(1, 1).tile() == 4
    assert world.agent(1, 1).mission() == 0
    
    assert str(world.agent(1, 1)) == "Carrier-1.1 ⌊(-0.18, 0.92), (0.18, 1.28)⌉ |0, 0|"

    world.render()
    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    # Turn 2
    game.playerHand(1)
    game.applyAction( "do 1", 1 )
    game.tic()

    assert world.agent(1, 1).tile() == 4
    assert world.agent(1, 1).mission() == 1
    assert str(world.agent(1, 1)) == "Carrier-1.1 ⌊(-0.18, 0.92), (0.18, 1.28)⌉ |0, 1|"

    # Turn 3-6
    moves= [12, 3, 3, 6]
    for m in moves :
        game.playerHand(1)
        game.applyAction( f"go {m}", 1 )
        game.tic()

    assert world.agent(1, 1).tile() == 5
    assert world.agent(1, 1).mission() == 1
    assert game.score(1) == -5.0

    # Turn 7
    game.playerHand(1)
    game.applyAction( "do 1 go 1", 1 )
    game.tic()

    assert world.agent(1, 1).tile() == 5
    assert world.agent(1, 1).mission() == 0
    assert game.score(1) == 119.0

def test_gamemaster_drawMissions():
    world= pnd.World()
    world.initializeGrid([
        [00, 00, 00, 00],
        [-1, 00, -1, -1],
        [00, 00, 00, 00],
        [00, -1, -1, 00]
    ])
    game= pnd.GameEngine( world, 1, tic=10 )
    world.teleport( world.agent(1, 1,).tile(), 1 )
    game.initialize()
    world.setMissions( [(4, 5), (7, 8)] )

    world.render()
    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    world.updateMission(1, 4, 5, 10, 1)

    world.render()
    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-04.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    world.updateMission(1, 0, 5, 0, 1)

    world.render()
    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-05.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    world.updateMission(2, 7, 8, 10, 1)
    world.updateMission(2, 0, 8, 0, 1)
    world.addMission(3, 6, 12)
    
    world.render()
    shotFile= open( "shot-pickndel.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-master-06.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gamemaster_distances_path():
    world= pnd.World()
    world.initializeGrid([
        [00, 00, 00, 00],
        [-1, 00, -1, -1],
        [00, 00, 00, 00],
        [00, -1, -1, 00]
    ])
    game= pnd.GameEngine( world, 1, tic=10 )
    game.initialize()
    world.setMissions( [(4, 5), (7, 8)] )

    assert game.world().size() == 11
    assert game.world()._distances == [
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

    assert game.toward(1, 2) == (3, 2)
    assert game.toward(4, 4) == (0, 4)
    assert game.toward(5, 11) == (6, 7)

    assert game.path(1, 11) == (
        [3, 6, 6, 3, 3, 6],
        [2, 5, 7, 8, 9, 11]
    )

def test_gamemaster_options():
    world= pnd.World()
    world.initializeGrid([
        [00, 00, 00, 00],  # 1  2  3  4
        [-1, 00, -1, -1],  #    5      
        [00, 00, 00, 00],  # 6  7  8  9
        [00, -1, -1, 00]   #10       13
    ])
    game= pnd.GameEngine( world, 1, tic=10 )
    game.initialize()
    world.setMissions( [(4, 5), (7, 8)] )

    world.render()

    #assert master.moveOptions(1, 2) == [(3, 2)]
    #assert master.moveOptions(4, 4) == [(0, 4)]
    #assert master.moveOptions(5, 11) == [(6, 8)]
    #assert master.moveOptions(5, 12) == [(3, 6), (6, 8)]

def test_gamemaster_loops():
    world= pnd.World()
    world.initializeGrid([
        [00, 00, 00, 00],  # 1  2  3  4
        [-1, 00, -1, -1],  #    5      
        [00, 00, 00, 00],  # 6  7  8  9
        [00, -1, -1, 00]   #10       13
    ])
    game= pnd.GameEngine( world, 1, tic=10 )
    world.teleport( world.agent(1, 1,).tile(), 1 )

    assert [ game.world().carrierTiles(i) for i in range(2) ] == [[], [1]]
    assert game.world()._missions  == []

    game.initialize()

    assert len( game.world()._missions ) == 1
    assert game.ticCounter() == 10

    game.setMoveAction(1, 1, 3)
    game.applyMoveActions()

    assert game._tic == 9
    assert game.world().carrierTiles(1) == [2]

    game.setMoveAction(1, 1, 6)
    game.applyMoveActions()

    assert game._tic == 8
    assert game.world().carrierTiles(1) == [5]

    assert game.playerScore(1) == -2.0
    
    game._scores= [0, 100.0]
    assert game.playerScore(1) == 100.0

    game.initialize()

    assert game._tic == 10
    assert game.world().carrierTiles(1) == [5]
    assert game.playerScore(1) == 0.0