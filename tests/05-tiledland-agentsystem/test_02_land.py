# HackaGames UnitTest - `pytest`
import sys, time
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tild
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_land_init():
    land= tild.Land()
    assert type(land) == tild.Land


def test_fast_land_first():
    land= tild.Land()
    land.map().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    assert type( land.box() ) == tild.Box

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-00.svg", mode='rb' ).read() )

    listOfUnits= [
        tild.Unit( Convex().initArrowTip(0.6), name= "X" ),
        tild.Unit( Convex().initArrowTip(0.4), name= "E" ),
        tild.Unit( Convex().initArrowTip(0.3), name= "C" )
    ]

    actorId= land.appendAgent( tild.Agent(), [9], [ listOfUnits[1].copy() ] )
    assert actorId == 1  

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-01.svg", mode='rb' ).read() )

    listOfUnits= tild.listOfDefaultUnits(4)
    
    actorId= land.appendAgent( tild.Agent() )
    selector= land.agentAddUnit( actorId, 3, listOfUnits[1].copy() )
    
    assert actorId == 2
    assert selector == (3, 1)

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-02.svg", mode='rb' ).read() )


def test_fast_land_popActor():
    land= tild.Land()
    land.map().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )

    bankOfUnits= tild.listOfArrowTipUnits( 
        [0.7, 0.4, 0.4,  0.2,   0.8, 0.6],
        [0.0, 0.0, 3.14, -1.57, 0.8, -2.6],
        ["x", "A", "B",  "C",   "D", "E"] )

    iAgent= land.appendAgent( tild.Agent(), 3, bankOfUnits[1])

    assert iAgent == 1
    assert iAgent == land.map().tile(3).unit(1).owner()

    land.appendAgent( tild.Agent(), 10, bankOfUnits[2].copy() )
    land.appendAgent( tild.Agent(), 12, bankOfUnits[3].copy() )
    land.appendAgent( tild.Agent(), 26, bankOfUnits[4].copy() )

    land.agentAddUnit( 0, 15, bankOfUnits[0].copy() )
    land.agentAddUnit( 3, 23, bankOfUnits[4].copy() )

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-03.svg", mode='rb' ).read() )

def test_fast_land_popBis():
    land= tild.Land()
    land.map().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )

    bankOfUnits= tild.listOfArrowTipUnits( 
        [0.4, 0.6, 0.6],
        [0.0, 3.14, -1.57],
        ["x", "A", "B"]
    )

    actor1= land.appendAgent( tild.Agent(), 15, bankOfUnits[1].copy() )

    assert actor1 == 1
    actor2= land.appendAgent( tild.Agent() )

    assert actor2 == 2
    assert len( land.interface(2).selectors() ) == 0

    land.agentAddUnit( actor2, 12, bankOfUnits[2].copy() )
    
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )

    assert len( land.interfaces() ) == 3 
    assert len( land.interface(0).selectors() ) == 0
    assert len( land.interface(1).selectors() ) == 1
    assert len( land.interface(2).selectors() ) == 1

    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )
    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-landpop-01.svg", mode='rb' ).read() )

    land.agentAddUnit( 0, 3, bankOfUnits[0].copy() )
    land.agentAddUnit( 0, 26, bankOfUnits[0].copy() )

    land.agentAddUnit( actor1, 6, bankOfUnits[1].copy() )
    land.agentAddUnit( actor1, 10, bankOfUnits[1].copy() )
    land.agentAddUnit( actor1, 21, bankOfUnits[1].copy() )

    land.agentAddUnit( actor2, 25, bankOfUnits[2].copy() )
    land.agentAddUnit( actor2, 30, bankOfUnits[2].copy() )

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    tild.drawMap( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-landpop-02.svg", mode='rb' ).read() )

    assert len( land.interfaces() ) == 3 
    assert len( land.interface(0).selectors() ) == 2
    assert len( land.interface(1).selectors() ) == 4
    assert len( land.interface(2).selectors() ) == 3

    assert [ (t) for t, u in land.interface(0).selectors() ] == [3, 26]
    assert [ (t) for t, u in land.interface(1).selectors() ] == [15, 6, 10 , 21]

def test_fast_land_orients():
    land= tild.Land()
    land.map().initHexa(
        [[-1, 0, 0], 
        [0, 0, 0], 
        [-1, 0, 0]], 1.4
    )

    land.appendAgent( tild.Agent(), 4, tild.Unit() )
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    
    bob= land.agentUnit(1, 1)
    
    assert round( bob.orientation(), 2) == 0.0

    land.actAgentOrient( 1, 1, tild.Action.DIR_W ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == 3.14
    
    land.actAgentOrient( 1, 1, tild.Action.DIR_SSE ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == -1.05

    land.actAgentRotateLeft( 1, 1 ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == -0.52

    land.actAgentRotateRight( 1, 1 ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == -1.05

    land.actAgentRotateRight( 1, 1, 4 ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == -3.14

    land.actAgentRotateRight( 1, 1, 2 ) 
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert round( bob.orientation(), 2) == 2.09

def test_fast_land_moves():
    land= tild.Land()
    land.map().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this selector
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )
    bankOfUnits= tild.listOfDefaultUnits()

    land.appendAgent( tild.Agent(), 15, bankOfUnits[1].copy() )
    land.agentAddUnit( 1, 29, bankOfUnits[1].copy() )
    land.appendAgent( tild.Agent(), 6, bankOfUnits[2].copy() )

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    
    print( str(land.agentUnit(1, 1)) )
    assert land.agentUnit(1, 1).strIdentity() == "A-1 1-0"
    assert land.interface(1).selector(1) == (15, 1)

    assert land.actAgentMove( 1, 1, 3 ) == (16, 1)
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert land.agentUnit(1, 1).strIdentity() == "A-1 1-0"
    assert land.interface(1).selector(1) == (16, 1)

    assert land.actAgentMove( 1, 1, 3 ) == (16, 1)
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert land.agentUnit(1, 1).strIdentity() == "A-1 1-0"
    assert land.interface(1).selector(1) == (16, 1)

    assert land.actAgentMove( 1, 1, tild.Action.DIR_NNE ) == (9, 1)
    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    assert land.agentUnit(1, 1).strIdentity() == "A-1 1-0"
    assert land.interface(1).selector(1) == (9, 1)
    assert round( land.agentUnit(1, 1).orientation(), 2 ) == 1.05

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )
    
    assert land.actAgentMove( 1, 2, tild.Action.DIR_W ) == (28, 1)
    assert land.actAgentMove( 1, 2, tild.Action.DIR_NNW ) == (22, 1)
    assert land.actAgentMove( 1, 2, tild.Action.DIR_NNW ) == (15, 1)
    assert land.actAgentMove( 1, 2, tild.Action.DIR_NNW ) == (8, 1)

    tild.drawMap( land.map(), "shot-test.png", 800, 600 )

    assert land.agentUnit(1, 1).strIdentity() == "A-1 1-0"
    assert land.interface(1).selector(1) == (9, 1)
    assert land.agentUnit(1, 2).strIdentity() == "A-2 1-0"
    assert land.interface(1).selector(2) == (8, 1)
    assert land.agentUnit(2, 1).strIdentity() == "B-1 2-0"
    assert land.interface(2).selector(1) == (6, 1)
    