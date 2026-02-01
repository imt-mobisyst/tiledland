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
    pablo= tll.Artist().initializeSVG( filePath= shotImg )

    shape= Convex().fromZipped( [(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    pablo.drawConvex( shape, 1 )
    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-01.svg" ).read()
    assert( shotFile == refsFile )

    pablo.drawConvex( shape, 0, -2.2, 2.2 )
    pablo.drawConvex( shape, 1, -1.1, 2.2 )
    pablo.drawConvex( shape, 2,   0, 2.2 )
    pablo.drawConvex( shape, 3, 1.1, 2.2 )
    pablo.drawConvex( shape, 4, 2.2, 2.2 )

    pablo.drawConvex( shape, 10, -2.2, 1.1 )
    pablo.drawConvex( shape, 11, -1.1, 1.1 )
    pablo.drawConvex( shape, 12,   0, 1.1 )
    pablo.drawConvex( shape, 13, 1.1, 1.1 )
    pablo.drawConvex( shape, 14, 2.2, 1.1 )

    pablo.drawConvex( shape, 5, -2.2, 0 )
    pablo.drawConvex( shape, 6, -1.1, 0 )
    pablo.drawConvex( shape, 7,   0, 0 )
    pablo.drawConvex( shape, 8, 1.1, 0 )
    pablo.drawConvex( shape, 9, 2.2, 0 )
    
    pablo.drawConvex( shape, 15, -2.2, -1.1 )
    pablo.drawConvex( shape, 16, -1.1, -1.1 )
    pablo.drawConvex( shape, 17,   0, -1.1 )
    pablo.drawConvex( shape, 18, 1.1, -1.1 )
    pablo.drawConvex( shape, 19, 2.2, -1.1 )

    pablo.drawConvex( shape, 20, -2.2, -2.2 )
    pablo.drawConvex( shape, 21, -1.1, -2.2 )
    pablo.drawConvex( shape, 74,   0, -2.2 )
    pablo.drawConvex( shape, 33, 1.1, -2.2 )
    pablo.drawConvex( shape, 42, 2.2, -2.2 )

    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-02.svg" ).read()
    assert( shotFile == refsFile )

def test_artist_png_load():
    shotImg= "shot-test.png"
    pablo= tll.Artist().initializePNG( filePath= shotImg )

    shape= Convex().fromZipped([(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    pablo.drawConvex( shape, 1 )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    pablo.drawConvex( shape, 0, -2.2, 0 )
    pablo.drawConvex( shape, 1, -1.1, 0 )
    pablo.drawConvex( shape, 2, 0, 0 )
    pablo.drawConvex( shape, 3, 1.1, 0 )
    pablo.drawConvex( shape, 4, 2.2, 0 )
    pablo.drawConvex( shape, 5, -0.55, 1.1 )
    pablo.drawConvex( shape, 6, 0.55, 1.1 )
    pablo.drawConvex( shape, 7, -0.55, -1.1 )
    pablo.drawConvex( shape, 8, 0.55, -1.1 )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/11.04-artist-panel-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
