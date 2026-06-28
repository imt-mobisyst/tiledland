# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_simulation_agent_init():
    agent= tll.Agent()
    assert agent.process(None) == None 


def test_fast_simulation_map_init():
    land= tll.Map()
    land.initHexa(
        [[0, 0, 0, -1, 0],    
        [0, -1, 0, 0, -1],    
        [0, 0, 0, -1, 0],     
        [0, 0, 0, -1, 0],      
        [-1, -1, 0, 0, 0]],
        1.4
    )

    # Create an artist to render this map:
    img= tll.createArtistPNG( "shot-test.png", 400, 300 )
    img.fitBox( land.box() )
    land.draw(img)
    img.flip() # Uptate the support and return to a blanc page.

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/05.01-land-00.png", mode='rb' ).read()
    #assert( shotFile == refsFile )

    # Add the agent:
    bod= land.popAgentOn(10)

    land.draw(img)
    img.flip()
    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/05.01-land-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    

