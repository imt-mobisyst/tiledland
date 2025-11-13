import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland.artist as artist

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #

# Test firstAI launch
def test_support_load():
    canvas= artist.AbsSupport()
    assert type( canvas ) == artist.AbsSupport

# Test firstAI launch
def test_support_color():
    assert artist.rgbColor( 0x56f4ee ) == (0x56, 0xf4, 0xee)
    assert artist.percentColor( 0x56f4ee ) == (0.3373, 0.9569, 0.9333)
    assert artist.webColor( 0x56f4ee ) == '#56f4ee'
    assert artist.colorFromWeb( '#56f4ee' ) == 0x56f4ee
    assert artist.color( 0x56, 0xf4, 0xee ) == 0x56f4ee

    assert artist.color( 0, 300, 128 ) == 0x00ff80

    print( artist.webColor( artist.colorRatio( 0x56f4ee, 0.1 ) ) )
    print( artist.webColor( artist.colorRatio( 0x56f4ee, 1.1 ) ) )

    assert artist.colorRatio( 0x56f4ee, 0.1 ) == 0x56f4ee
    assert artist.colorRatio( 0x56f4ee, 1.1 ) == 0x56f4ee

# Test firstAI launch
def test_artist_load():
    pablo= artist.Artist()
    assert type( pablo ) == artist.Artist

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

    print( pablo.content() )
    assert pablo.content() == """<polygon points="0,0 0,600 800,600 800,0" fill="#b86e00" />
<circle r="4" cx="2600.0" cy="1100.0" fill="#991100" />
<line x1="2600.0" y1="1100.0" x2="1850.0" y2="-40.0" style="stroke:#991100;stroke-width:4"/>
<circle r="1470.0" cx="2600.0" cy="1100.0" fill="none" stroke="#991100" stroke-width="4" />
<circle r="1470.0" cx="2600.0" cy="1100.0" fill="#ff6644" />
<circle r="1470.0" cx="2600.0" cy="1100.0" fill="#ff6644" stroke="#991100" stroke-width="4" />
<polygon points="2600.0,-900.0 -400.0,-500.0 1870.0,-109.99999999999994" style="fill:none;stroke:#991100;stroke-width:4" />
<polygon points="2600.0,-900.0 -400.0,-500.0 1870.0,-109.99999999999994" fill="#ff6644" />
<polygon points="2600.0,-900.0 -400.0,-500.0 1870.0,-109.99999999999994" style="fill:#ff6644;stroke:#991100;stroke-width:4" />
<line x1="100.0" y1="10" x2="100.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="200.0" y1="10" x2="200.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="300.0" y1="10" x2="300.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="400.0" y1="10" x2="400.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="500.0" y1="10" x2="500.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="600.0" y1="10" x2="600.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="700.0" y1="10" x2="700.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="800.0" y1="10" x2="800.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="900.0" y1="10" x2="900.0" y2="590" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="100.0" x2="790" y2="100.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="200.0" x2="790" y2="200.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="300.0" x2="790" y2="300.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="400.0" x2="790" y2="400.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="500.0" x2="790" y2="500.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="600.0" x2="790" y2="600.0" style="stroke:#603800;stroke-width:2"/>
<line x1="10" y1="700.0" x2="790" y2="700.0" style="stroke:#603800;stroke-width:2"/>
<line x1="400.0" y1="300.0" x2="500.0" y2="300.0" style="stroke:#e26060;stroke-width:6"/>
<line x1="400.0" y1="300.0" x2="400.0" y2="200.0" style="stroke:#60e260;stroke-width:6"/>
<circle r="6" cx="400.0" cy="300.0" fill="#0606e2" />"""
    
    assert pablo.render() == f'<svg width="800" height="600">\n{pablo.content()}\n</svg>'

