import sys, hacka.py as hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll

def test_players_basic():
    game= mi.GameEngine(
        numberOfRobots= 2,
        missions= [(4, 5), (7, 8)],
    )

    master= mi.GameMaster( game )
    bot= player.BasicBot()
    bot.wakeUp( 1, 2, master.initialize() )
    
    assert bot.model().numberOfMobiles() == 2

    bot.perceive( master.playerHand(1) )
    assert bot.decide() == "pass"

    assert bot.model().asPod().dump() == game.asPod().dump()

    bot.model().render()
    local.sleep()


def test_players_basic():
    game= mi.GameEngine(
        missions= [(4, 5), (7, 8)],
        tic= 10 )
    master= mi.GameMaster( game )

    assert master._engine.missionsList() == [1, 2]
    assert master.initialize()

    t= 10
    while t > 0 :
        assert not master.isEnded()
        assert game.tic() == t
        master.tic()
        t-= 1
    
    assert( master.isEnded() )

def test_players_updateFromState():
    player= mi.BlindBot( ['mission 1 4', 'move 1 6', 'pass'] )
    #player= mi.BasicBot()
    
    gameConfigDump= """MoveIt - 0 4 3 2 : 2 1 0 20 0.0 0.0 0.0
Map - 0 0 0 11 :
Shape - 0 1 16 0 : 0 -0.29 0.12 -0.12 0.29 0.12 0.29 0.29 0.12 0.29 -0.12 0.12 -0.29 -0.12 -0.29 -0.29 -0.12
Tile - 0 5 10 1 : 1 0 1 2 4 0.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
R-1 - 0 3 0 0 : 1 1 0
Tile - 0 6 10 1 : 2 0 1 2 3 5 1.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
R-1 - 0 3 0 0 : 2 1 0
Tile - 0 4 10 0 : 3 0 2 3 2.0 3.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 6 10 0 : 4 0 1 4 5 6 0.0 2.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 6 10 0 : 5 0 2 4 5 7 1.0 2.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 6 10 0 : 6 0 4 6 7 9 0.0 1.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 6 10 0 : 7 0 5 6 7 8 1.0 1.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 5 10 0 : 8 0 7 8 10 2.0 1.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 9 0 6 9 0.0 0.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
Tile - 0 4 10 0 : 10 0 8 10 2.0 0.0 -0.45 0.45 0.45 0.45 0.45 -0.45 -0.45 -0.45
missions - 0 0 0 4 :
1 - 0 4 0 0 : 9 9 10 0
2 - 0 4 0 0 : 3 8 10 0
3 - 0 4 0 0 : 10 7 10 0
4 - 0 4 0 0 : 2 9 10 0
"""
    configPod= hk.Pod().load( gameConfigDump )

    player.wakeUp( 2, 2, configPod )

    assert str(configPod) == str(player._model.asPod()) 

    assert type(player._model.mobile(1, 0)) == mi.Mobile
    assert player._model.mobileMission(1, 0) == 0

    assert( len( player._model._map._mobiles ) == 3 )
    assert( len( player._model._map._mobiles[1] ) == 1 )
    assert( len( player._model._map._mobiles[2] ) == 1 )

    stateDumps= [
"""State - 0 1 3 2 : 20 0.0 0.0 0.0
missions - 0 0 0 4 :
1 - 0 4 0 0 : 9 9 10 0
2 - 0 4 0 0 : 3 8 10 0
3 - 0 4 0 0 : 10 7 10 0
4 - 0 4 0 0 : 2 9 10 0
mobiles - 0 0 0 2 :
Pod - 0 4 0 0 : 1 1 1 0
Pod - 0 4 0 0 : 2 1 2 0
""",
"""State - 0 1 3 2 : 19 0.0 -100.0 0.0
missions - 0 0 0 4 :
1 - 0 4 0 0 : 9 9 10 0
2 - 0 4 0 0 : 3 8 10 0
3 - 0 4 0 0 : 10 7 10 0
4 - 0 4 0 0 : 2 9 10 2
mobiles - 0 0 0 2 :
Pod - 0 4 0 0 : 1 1 1 0
Pod - 0 4 0 0 : 2 1 2 4
""",    
"""State - 0 1 3 2 : 18 0.0 -200.0 0.0
missions - 0 0 0 4 :
1 - 0 4 0 0 : 9 9 10 0
2 - 0 4 0 0 : 3 8 10 0
3 - 0 4 0 0 : 10 7 10 0
4 - 0 4 0 0 : 2 9 10 2
mobiles - 0 0 0 2 :
Pod - 0 4 0 0 : 1 1 1 0
Pod - 0 4 0 0 : 2 1 5 4
"""
    ]

    for sd in stateDumps :
        statePod= hk.Pod().load( sd )
        player.perceive( statePod )
        player.decide()
        assert( len( player._model._map._mobiles ) == 3 )
        assert( len( player._model._map._mobiles[1] ) == 1 )
        assert( len( player._model._map._mobiles[2] ) == 1 )

    #assert False

def test_players_2players():
    # Configure the game:
    gameEngine= mi.GameEngine(
        matrix= [ [00, 00, 00],
                [00, 00, -1],
                [00, 00, 00],
                [00, -1, 00] ],
        numberOfPlayers=2, numberOfRobots=1, tic= 20,
        missions= [(9, 9), (3, 8), (10, 7), (2, 9)]
    )

    # Then Go...
    gameMaster= mi.GameMaster( gameEngine )

    players= [
        mi.BlindBot(['move 1 3', 'move 1 3', 'move 1 6']),
        mi.BlindBot(['mission 1 4', 'move 1 6', 'pass'])
    ]
    
    gameConf= gameMaster.initialize()
    #print( "---" )
    #print( gameConf.dump() )
    #print( "---" )

    # wakeUpPlayers
    iPlayer= 1
    for player in players :
        player.wakeUp( iPlayer, 2, hk.Pod().load( gameConf.dump() ) )
        #player.wakeUp( iPlayer, 2, gameConf )
        iPlayer+= 1
    
    # player take turns :
    iPlayer= 1
    while not gameMaster.isEnded() :
        # activatePlayer :
        stateDump= gameMaster.playerHand(iPlayer).asPod().dump()
        #print( f"---{iPlayer}" )
        #print( stateDump )
        #print( "---" )
    
        players[iPlayer-1].perceive( hk.Pod().load(stateDump) )

        assert str(gameMaster._engine.asPod()) == str(players[iPlayer-1]._model.asPod())
        gameMaster._engine.render()

        gameMap= gameMaster._engine._map
        playerMap= players[iPlayer-1]._model._map

        assert( len( gameMap._mobiles ) == 3 )
        assert( len( gameMap._mobiles[1] ) == 1 )
        assert( len( gameMap._mobiles[2] ) == 1 )

        assert( len( playerMap._mobiles ) == 3 )
        assert( len( playerMap._mobiles[1] ) == 1 )
        assert( len( playerMap._mobiles[2] ) == 1 )

        action= players[iPlayer-1].decide()
        assert( gameMaster.applyPlayerAction( iPlayer, action ) )
        iPlayer+= 1
        # End turn ?
        if iPlayer > 2 :
            gameMaster.tic()
            iPlayer= 1
    # conclude the game :
    iPlayer= 1
    while iPlayer <= 2 :
        # sleepPlayer( iPlayer, self.playerHand(iPlayer), self.playerScore(iPlayer) )
        players[iPlayer-1].perceive( hk.Pod().load( gameMaster.playerHand(iPlayer).asPod().dump() ) )
        players[iPlayer-1].sleep( gameMaster.playerScore(iPlayer) )
        iPlayer+= 1

def test_players_2playersBis():
    # Configure the game:
    gameEngine= mi.GameEngine(
        matrix= [ [00, 00, 00],
                [00, 00, -1],
                [00, 00, 00],
                [00, -1, 00] ],
        numberOfPlayers=2, numberOfRobots=1, tic= 20,
        missions= [(9, 9), (3, 8), (10, 7), (2, 9)]
    )

    # Then Go...
    gameMaster= mi.GameMaster( gameEngine )
    gameMaster.launch( [mi.BlindBot(['move 1 3', 'move 1 3', 'move 1 6']), mi.BlindBot(['mission 1 4', 'move 1 6', 'pass'])] )
