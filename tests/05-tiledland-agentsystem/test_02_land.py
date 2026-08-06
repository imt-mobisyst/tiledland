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

    land.initializeArrowTipBankOfEntities( range(5),
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

def test_fast_land_multi_bodies():
    assert True
