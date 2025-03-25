import sys, hacka.py as hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

matrix= [
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
    [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
    [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
    [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
]

missions= [
    ( 19, 48 ), ( 43, 28 ), ( 43, 40 ),
    ( 22, 34 ), ( 35, 25 ), ( 10, 12 ),
    ( 14, 12 ), ( 29, 34 ), ( 12, 44 ),
    ( 29, 34 ), ( 12, 36 )
]

def test_gameengine_init():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game._map.tile(1).adjacencies() == [1, 2, 4]
    assert game._map.tile(2).adjacencies() == [1, 2, 3]
    assert game._map.tile(8).adjacencies() == [5, 7, 8]
    

def test_gameengine_initLarge():
    game= mi.GameEngine( matrix, 2, 3, 1 )

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_move():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.tic() == 100
    assert game.moveActions( 1 ) == [0]
    assert game.setMoveAction( 1, 1, 6 )
    assert game.moveActions( 1 ) == [6]

    assert game._map.mobilePositions(1) == [1]

    game.applyMoveActions()
    assert game.tic() == 99

    assert game._map.mobilePositions(1) == [4]

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.moveActions(1) == [0]
    assert game.setMoveAction( 1, 1, 3 )
    assert game.moveActions(1) == [3]

    game.applyMoveActions()
    assert game.tic() == 98

    assert game._map.mobilePositions(1) == [4]

    game.render()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_mission():
    game= mi.GameEngine()

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.freeMissions() == []
    
    assert game.addMission( 4, 5 ) == 1
    assert game.addMission( 7, 8 ) == 2

    assert game.freeMissions() == [1, 2]

    assert game.mission(1).tuple() == (4, 5, 10, 0)
    assert game.mission(2).tuple() == (7, 8, 10, 0)

    game.render()
    local.sleep()
    
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-04.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.missionAction(1, 1, 1) == False

    assert game.mobile(1, 1).mission() == 0

    game.setMoveAction( 1, 1, 6 )
    game.applyMoveActions()
    assert game.tic() == 99

    assert game.missionAction(1, 1, 1) == True

    assert game.mobile(1, 1).mission() == 1

    assert game.freeMissions() == [2]

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-05.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    game.setMoveAction( 1, 1, 6 )
    game.applyMoveActions()

    game.setMoveAction( 1, 1, 3 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 7

    assert game.missionAction(1, 1, 1) == False
    assert game.missionAction(1, 1, 2) == False

    game.setMoveAction( 1, 1, 3 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 8

    game.setMoveAction( 1, 1, 12 )
    game.applyMoveActions()

    assert game.mobilePosition(1, 1) == 5
    assert game.mobile(1, 1).mission() == 1
    assert game.missionAction(1, 1, 1) == True
    assert game.missionAction(1, 1, 2) == False

    assert game.mobile(1, 1).mission() == 0
    assert game.freeMissions() == [2]

    assert game.tic() == 95

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-06.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_collisions():
    game= mi.GameEngine( matrix, 2, 3, 0 )

    i= 1
    for iFrom, iTo in missions :
        assert game.addMission( iFrom, iTo ) == i
        i+= 1

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-07.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game._map.mobilePositions(0) == []
    assert game._map.mobilePositions(1) == [1, 2, 3]
    assert game._map.mobilePositions(2) == [4, 5, 6]

    game.setMoveAction( 1, 1, 6 )
    game.setMoveAction( 1, 2, 0 )
    game.setMoveAction( 1, 3, 6 )
    
    game.setMoveAction( 2, 1, 6 )
    game.setMoveAction( 2, 2, 0 )
    game.setMoveAction( 2, 3, 6 )

    assert game.applyMoveActions() == 0

    assert game._map.mobilePositions(1) == [10, 2, 11]
    assert game._map.mobilePositions(2) == [13, 5, 14]

    game.setMoveAction( 1, 1, 12 )
    game.setMoveAction( 1, 2, 9 )
    game.setMoveAction( 1, 3, 3 )
    
    game.setMoveAction( 2, 1, 12 )
    game.setMoveAction( 2, 2, 3 )
    game.setMoveAction( 2, 3, 0 )

    assert game.applyMoveActions() == 2

    assert game._map.mobilePositions(1) == [10, 2, 12]
    assert game._map.mobilePositions(2) == [4, 6, 14]

    game.setMoveAction( 2, 1, 3 )
    game.setMoveAction( 2, 2, 6 )
    game.setMoveAction( 2, 3, 6 )

    assert game.applyMoveActions() == 1

    assert game._map.mobilePositions(1) == [10, 2, 12]
    assert game._map.mobilePositions(2) == [5, 6, 21]


def test_gameengine_score():
    game= mi.GameEngine( matrix, 2, 3, 0, missions= missions )

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-07.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    assert game.score(1) == 0
    assert game.score(2) == 0

    game.setMoveAction( 1, 1, 6 )
    game.setMoveAction( 1, 3, 6 )
    
    game.setMoveAction( 2, 1, 6 )
    game.setMoveAction( 2, 3, 6 )

    assert game.applyMoveActions() == 0
    
    assert game.score(1) == 0
    assert game.score(2) == 0

    assert game._map.mobilePositions(1) == [10, 2, 11]
    assert game._map.mobilePositions(2) == [13, 5, 14]

    game.setMoveAction( 1, 1, 12 )
    game.setMoveAction( 1, 2, 9 )
    game.setMoveAction( 1, 3, 3 )
    
    game.setMoveAction( 2, 1, 12 )
    game.setMoveAction( 2, 2, 3 )
    game.setMoveAction( 2, 3, 0 )

    assert game.applyMoveActions() == 2
    
    assert game.score(1) == -200
    assert game.score(2) == 0

    assert game._map.mobilePositions(1) == [10, 2, 12]
    assert game._map.mobilePositions(2) == [4, 6, 14]

    game.missionAction( 1, 3, 11 )
    game.setMoveAction( 2, 1, 3 )
    game.setMoveAction( 2, 2, 6 )
    game.setMoveAction( 2, 3, 6 )

    assert game.applyMoveActions() == 1

    assert game.score(1) == -200
    assert game.score(2) == -100

    game._map.teleport( 12, 36 )
    game._map.teleport( 5, 17 )

    game.missionAction( 1, 3, 11 )
    game.addMission( 30, 4, 70 )

    assert game.score(1) == -190
    assert game.score(2) == -100

    game.setMoveAction( 1, 1, 6 )
    game.setMoveAction( 2, 1, 9 )

    assert game.applyMoveActions() == 2

    assert game.score(1) == -290
    assert game.score(2) == -200

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-08.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_gameengine_podInterface():
    game= mi.GameEngine( missions= [(3, 8)] )
    
    game._map.teleport( 1, 4 )

    pod= game.asPod()

    #print( f'"""{pod}"""' )
    
    assert str(pod) == """MoveIt: [1, 1, 0, 100] [0.0, 0.0]
- Map:
  - Shape: [0] [-0.29, 0.12, -0.12, 0.29, 0.12, 0.29, 0.29, 0.12, 0.29, -0.12, 0.12, -0.29, -0.12, -0.29, -0.29, -0.12]
  - Tile: [1, 0, 1, 2, 4] [0.0, 2.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [2, 0, 1, 2, 3] [1.0, 2.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [3, 0, 2, 3, 5] [2.0, 2.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [4, 0, 1, 4, 6] [0.0, 1.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
    - R-1: [1, 1, 0]
  - Tile: [5, 0, 3, 5, 8] [2.0, 1.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [6, 0, 4, 6, 7] [0.0, 0.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [7, 0, 6, 7, 8] [1.0, 0.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
  - Tile: [8, 0, 5, 7, 8] [2.0, 0.0, -0.45, 0.45, 0.45, 0.45, 0.45, -0.45, -0.45, -0.45]
- missions:
  - 1: [3, 8, 10, 0]"""

    game2= mi.GameEngine()
    game2.fromPod(pod)

    assert game2.mobilePosition(1, 1) == 4
    assert type( game2.mobile(1, 1) ) == mi.Mobile
    assert game2.mobile(1, 1).owner() == 1

    #print( f'"""{game2.asPod()}"""' )

    assert str( game2.asPod() ) == str( pod )

    state= game2.state()
    print( f'"""{state}"""' )
    assert str(state) == """State: [100] [0.0, 0.0]
- missions:
  - 1: [3, 8, 10, 0]
- mobiles:
  - Pod: [1, 1, 4, 0]"""

    stateBis= mi.GameEngine().setOnState(state).state()
    print( f'"""{stateBis}"""' )
    assert str(stateBis) == str(state)

def test_gameengine_podInterface2():
    game= mi.GameEngine( matrix, 2, 3, 0, missions= missions )
    pod= game.asPod()

    game2= mi.GameEngine()
    game2.fromPod( pod )

    assert str( game2.asPod() ) == str( pod )

    game.render()
    local.sleep()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/02-engine-07.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    game._scores= [0, 120, 90]

    game.setMoveAction( 1, 1, 6 )
    game.setMoveAction( 1, 3, 6 )
    game.setMoveAction( 2, 1, 6 )
    game.setMoveAction( 2, 3, 6 )
    game.applyMoveActions()

    print( f'"""{game.state()}"""' )

    game2.setOnState( game.state() )

    assert game2.score(1) == 120
    assert game2.score(2) == 90
    assert game2._map.mobilePositions(1) == [10, 2, 11]
    assert game2._map.mobilePositions(2) == [13, 5, 14]

    assert str( game2.asPod() ) == str( game.asPod() )
