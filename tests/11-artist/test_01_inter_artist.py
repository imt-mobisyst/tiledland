import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland.artist as hka

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #

# Test firstAI launch
def test_support_load():
    canvas= hka.SupportVoid()
    assert type( canvas ) == hka.SupportVoid

# Test firstAI launch
def test_support_color():
    assert hka.rgbColor( 0x56f4ee ) == (0x56, 0xf4, 0xee)
    assert hka.percentColor( 0x56f4ee ) == (0.3373, 0.9569, 0.9333)
    assert hka.webColor( 0x56f4ee ) == '#56f4ee'
    assert hka.colorFromWeb( '#56f4ee' ) == 0x56f4ee
    assert hka.color( 0x56, 0xf4, 0xee ) == 0x56f4ee

    assert hka.color( 0, 300, 128 ) == 0x00ff80

    print( hka.webColor( hka.colorRatio( 0x56f4ee, 0.1 ) ) )
    print( hka.webColor( hka.colorRatio( 0x56f4ee, 1.1 ) ) )

    assert hka.colorRatio( 0x56f4ee, 0.1 ) == 0x56f4ee
    assert hka.colorRatio( 0x56f4ee, 1.1 ) == 0x56f4ee

# Test firstAI launch
def test_artist_load():
    pablo= hka.Artist()
    assert type( pablo ) == hka.Artist

    pablo.tracePoint( 22.0, -8 )
    pablo.traceLine( 22.0, -8, 14.5, 3.4 )
    pablo.traceCircle( 22.0, -8, 14.7 )
    pablo.fillCircle( 22.0, -8, 14.7 )
    pablo.drawCircle( 22.0, -8, 14.7 )
    pablo.tracePolygon( [22.0, -8, 14.7], [12.0, 8, 4.1] )
    pablo.fillPolygon( [22.0, -8, 14.7], [12.0, 8, 4.1] )
    pablo.drawPolygon( [22.0, -8, 14.7], [12.0, 8, 4.1] )
    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    assert( pablo.render() == None )

