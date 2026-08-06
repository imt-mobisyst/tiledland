# HackaGames UnitTest - `pytest`
import sys, time
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_land_init():
    land= tll.Land()
    assert type(land) == tll.Land

def test_fast_land_first():
    land= tll.Land()
    land.tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )
    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-00.svg", mode='rb' ).read() )

    actorId= land.appendActor( tll.Agent(),
        [9], [tll.Entity(0, Convex().initArrowTip(0.4), name="E")]
    )
    assert actorId == 1  

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )
    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-01.svg", mode='rb' ).read() )

    land.initializeDefaultBankOfEntities(4)

    actorId= land.appendActor( tll.Agent() )
    land.popActorBody( actorId, 3, 1 )
    
    assert actorId == 2

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )
    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-02.svg", mode='rb' ).read() )

def test_fast_land_popActor():
    land= tll.Land()
    land.tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )

    land.initializeArrowTipBankOfEntities( range(1, 6),
        [0.4, 0.4, 0.2, 0.8, 0.6],
        [0.0, 3.14, -1.57, 0.8, -2.6],
        ["A", "B", "C", "D", "E"] )

    land.popSimpleActor( tll.Agent(), 3, 1 )
    land.popSimpleActor( tll.Agent(), 10, 2 )
    land.popSimpleActor( tll.Agent(), 12, 3 )
    land.popSimpleActor( tll.Agent(), 15, 0 )
    land.popSimpleActor( tll.Agent(), 26, 4 )

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )
    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-03.svg", mode='rb' ).read() )

def test_fast_land_popActor():
    land= tll.Land()
    land.tabletop().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )

    land.initializeArrowTipBankOfEntities( range(3),
        [0.4, 0.6, 0.6],
        [0.0, 3.14, -1.57],
        ["X", "A", "B"] )

    actor1= land.popSimpleActor( tll.Agent(), 15, 1 )

    assert actor1 == 1
    actor2= land.appendActor( tll.Agent() )

    assert actor2 == 2
    assert len( land.actor(2).bodies() ) == 0

    land.popActorBody( actor2, 12, 2 )
    
    assert actor2 == 2

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )

    assert len( land.actors() ) == 3 
    assert len( land.actor(0).bodies() ) == 0
    assert len( land.actor(1).bodies() ) == 1
    assert len( land.actor(2).bodies() ) == 1

    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )
    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-landpop-01.svg", mode='rb' ).read() )

    land.popActorBody( 0, 3, 0 )
    land.popActorBody( 0, 26, 0 )

    land.popActorBody( actor1, 6, 1 )
    land.popActorBody( actor1, 10, 1 )
    land.popActorBody( actor1, 21, 1)

    land.popActorBody( actor2, 25, 2 )
    land.popActorBody( actor2, 30, 2 )

    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )
    tll.draw( land.tabletop(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-landpop-02.svg", mode='rb' ).read() )

    assert len( land.actors() ) == 3 
    assert len( land.actor(0).bodies() ) == 2
    assert len( land.actor(1).bodies() ) == 4
    assert len( land.actor(2).bodies() ) == 3

    assert [ (b.location()) for b in land.actor(0).bodies() ] == [3, 26]
    assert [ (b.location()) for b in land.actor(1).bodies() ] == [15, 6, 10 , 21]


def test_fast_land_moves():


    assert land.clockBearing(44) == [9, 3]

    assert land.move( 44, 12 ) == False
    assert land.move( 44, 3 ) == 45
    assert land.move( 45, 12 ) == 39
    assert land.move( 39,  0 ) == 39
    assert land.move( 39,  3 ) == False


    assert False
