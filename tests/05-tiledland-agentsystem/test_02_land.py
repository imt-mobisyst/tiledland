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
    land.map().initHexa(
        [[0, 0, 0, -1, 0, 0, 0, 0],     #   -1   : means no cell at this location
        [0, -1, 0, 0, 0, -1, 0, 0],     #  0 - n : give the group identifier of the cell to create.
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [0, 0, 0, -1, 0, 0, 0, 0],      #  
        [-1, -1, 0, 0, 0, -1, -1, -1]]  #
    )

    tll.draw( land.map(), "shot-test.png", 800, 600 )
    tll.draw( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-00.svg", mode='rb' ).read() )

    identifier= land.tileAppendAvatar( 9,
        tll.Entity(0, Convex().initArrowTip(0.4), name="E"),
        tll.Agent()
    )
    assert identifier == 1  

    tll.draw( land.map(), "shot-test.png", 800, 600 )
    tll.draw( land.map(), "shot-test.svg", 800, 600 )

    assert( open( "shot-test.svg", mode='rb' ).read()
        == open( "tests/refs/05.02-land-01.svg", mode='rb' ).read() )

#def test_fast_land_factory():
#    assert False