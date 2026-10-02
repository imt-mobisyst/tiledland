import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tild
from src.tiledland.geometry import Point, Convex
from src.tiledland.artist import palette00, palette01

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #

# Test firstAI launch
def test_fast_artist_palette():
    shotImg= "shot-test.svg"
    pablo= tild.artist.openSVG( shotImg, 800, 600 )

    shape= Convex().fromZipped( [(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    pablo.drawConvex( shape, palette00[1] )
    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/02.04-palette-01.svg" ).read()
    assert( shotFile == refsFile )

    pablo.drawConvex( shape,  palette00[0], -2.2, 1.7 )
    pablo.drawConvex( shape,  palette00[1], -1.1, 1.7 )
    pablo.drawConvex( shape,  palette00[2],    0, 1.7 )
    pablo.drawConvex( shape,  palette00[3],  1.1, 1.7 )
    pablo.drawConvex( shape,  palette00[4],  2.2, 1.7 )

    pablo.drawConvex( shape,  palette01[0], -2.2, 0.6 )
    pablo.drawConvex( shape,  palette01[1], -1.1, 0.6 )
    pablo.drawConvex( shape,  palette01[2],    0, 0.6 )
    pablo.drawConvex( shape,  palette01[3],  1.1, 0.6 )
    pablo.drawConvex( shape,  palette01[4],  2.2, 0.6 )

    pablo.drawConvex( shape,  palette00[5], -2.2, -0.5 )
    pablo.drawConvex( shape,  palette00[6], -1.1, -0.5 )
    pablo.drawConvex( shape,  palette00[7],    0, -0.5 )
    pablo.drawConvex( shape,  palette00[8],  1.1, -0.5 )
    pablo.drawConvex( shape,  palette00[9],  2.2, -0.5 )
    
    pablo.drawConvex( shape,  palette01[5], -2.2, -1.6 )
    pablo.drawConvex( shape,  palette01[6], -1.1, -1.6 )
    pablo.drawConvex( shape,  palette01[7],    0, -1.6 )
    pablo.drawConvex( shape,  palette01[8],  1.1, -1.6 )
    pablo.drawConvex( shape,  palette01[9],  2.2, -1.6 )

    pablo.flip()
    
    shotFile= open( shotImg ).read() 
    refsFile= open( "tests/refs/02.04-palette-02.svg" ).read()
    assert( shotFile == refsFile )

def test_fast_artist_palette_png():
    shotImg= "shot-test.png"
    pablo= tild.artist.openPNG(shotImg, 800, 600)

    shape= Convex().fromZipped([(-0.5, -0.5),  (0.5, -0.5),  (0.5, 0.5),  (-0.5, 0.5)] )
    pablo.drawConvex( shape, palette00[1] )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/02.04-palette-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    pablo.drawConvex( shape,  palette00[0], -2.2, 0 )
    pablo.drawConvex( shape,  palette00[1], -1.1, 0 )
    pablo.drawConvex( shape,  palette00[2], 0, 0 )
    pablo.drawConvex( shape,  palette00[3], 1.1, 0 )
    pablo.drawConvex( shape,  palette00[4], 2.2, 0 )
    pablo.drawConvex( shape,  palette00[5], -0.55, 1.1 )
    pablo.drawConvex( shape,  palette00[6], 0.55, 1.1 )
    pablo.drawConvex( shape,  palette00[7], -0.55, -1.1 )
    pablo.drawConvex( shape,  palette00[8], 0.55, -1.1 )
    pablo.flip()
    
    shotFile= open( shotImg, mode='rb' ).read() 
    refsFile= open( "tests/refs/02.04-palette-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )
