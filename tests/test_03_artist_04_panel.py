import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tll
from src.tiledland.geometry import Point, Convex

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #

# Test firstAI launch
def test_artist_svg_load():
    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG( shotImg, 800, 600 )

    shape= Convex().fromZipped( [(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    shape.draw( pablo, 1 )
    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-01.svg" ).read()
    assert( shotFile == refsFile )

    shape.draw( pablo, 0, -2.2, 2.2 )
    shape.draw( pablo, 1, -1.1, 2.2 )
    shape.draw( pablo, 2,   0, 2.2 )
    shape.draw( pablo, 3, 1.1, 2.2 )
    shape.draw( pablo, 4, 2.2, 2.2 )

    shape.draw( pablo, 10, -2.2, 1.1 )
    shape.draw( pablo, 11, -1.1, 1.1 )
    shape.draw( pablo, 12,   0, 1.1 )
    shape.draw( pablo, 13, 1.1, 1.1 )
    shape.draw( pablo, 14, 2.2, 1.1 )

    shape.draw( pablo, 5, -2.2, 0 )
    shape.draw( pablo, 6, -1.1, 0 )
    shape.draw( pablo, 7,   0, 0 )
    shape.draw( pablo, 8, 1.1, 0 )
    shape.draw( pablo, 9, 2.2, 0 )
    
    shape.draw( pablo, 15, -2.2, -1.1 )
    shape.draw( pablo, 16, -1.1, -1.1 )
    shape.draw( pablo, 17,   0, -1.1 )
    shape.draw( pablo, 18, 1.1, -1.1 )
    shape.draw( pablo, 19, 2.2, -1.1 )

    shape.draw( pablo, 20, -2.2, -2.2 )
    shape.draw( pablo, 21, -1.1, -2.2 )
    shape.draw( pablo, 74,   0, -2.2 )
    shape.draw( pablo, 33, 1.1, -2.2 )
    shape.draw( pablo, 42, 2.2, -2.2 )

    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-02.svg" ).read()
    assert( shotFile == refsFile )

def test_artist_png_load():
    shotImg= "shot-test.png"
    pablo= tll.createArtistPNG(shotImg, 800, 600)

    shape= Convex().fromZipped([(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    shape.draw( pablo, 1 )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    shape.draw( pablo, 0, -2.2, 0 )
    shape.draw( pablo, 1, -1.1, 0 )
    shape.draw( pablo, 2, 0, 0 )
    shape.draw( pablo, 3, 1.1, 0 )
    shape.draw( pablo, 4, 2.2, 0 )
    shape.draw( pablo, 5, -0.55, 1.1 )
    shape.draw( pablo, 6, 0.55, 1.1 )
    shape.draw( pablo, 7, -0.55, -1.1 )
    shape.draw( pablo, 8, 0.55, -1.1 )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
