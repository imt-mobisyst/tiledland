import sys
workDir= __file__.split('/tests/')[0]
sys.path.insert( 1, workDir )

import src.tiledland as tll

# ------------------------------------------------------------------------ #
#                 T E S T   I N T E R F A C E    A R T I S T
# ------------------------------------------------------------------------ #

# Test firstAI launch
def test_support_load():
    sup= tll.SupportSVG()
    assert( type(sup) ) == tll.SupportSVG

    print( sup.render() )
    assert( sup.render() == """<svg width="800" height="600">
</svg>""" )

# Test firstAI launch
def test_support_draw():
    suppo= tll.SupportSVG()
    
    assert( suppo.render() == """<svg width="800" height="600">
</svg>""" )

    suppo.traceLine( -40, 8, 240, 80, 0x25e3f2, 3 )

    print( "---\n" + suppo.render() )
    assert( suppo.render() == """<svg width="800" height="600">
<line x1="-40" y1="8" x2="240" y2="80" style="stroke:#25e3f2;stroke-width:3"/>
</svg>""" )

    suppo.traceCircle( 50, 50, 32, 0x25e3f2, 3 )
    suppo.fillCircle( 100, 50, 32, 0x25e302 )
    suppo.drawCircle( 150, 50, 44, 0x25e302, 0x25e3f2, 8)
    
    assert( suppo.render() == """<svg width="800" height="600">
<line x1="-40" y1="8" x2="240" y2="80" style="stroke:#25e3f2;stroke-width:3"/>
<circle r="32" cx="50" cy="50" fill="none" stroke="#25e3f2" stroke-width="3" />
<circle r="32" cx="100" cy="50" fill="#25e302" />
<circle r="44" cx="150" cy="50" fill="#25e302" stroke="#25e3f2" stroke-width="8" />
</svg>""" )

    suppo.fillPolygon( [30, 140, 70], [130, 130, 200], 0x25e302 )
    suppo.drawPolygon( [70, 190, 130], [130, 130, 200], 0x25e302, 0x25e3f2, 4 )
    suppo.tracePolygon( [10, 10, 790, 790], [10, 590, 590, 10], 0x25e3f2, 6 )

    print( "---\n" + suppo.render() )
    assert( suppo.render() == """<svg width="800" height="600">
<line x1="-40" y1="8" x2="240" y2="80" style="stroke:#25e3f2;stroke-width:3"/>
<circle r="32" cx="50" cy="50" fill="none" stroke="#25e3f2" stroke-width="3" />
<circle r="32" cx="100" cy="50" fill="#25e302" />
<circle r="44" cx="150" cy="50" fill="#25e302" stroke="#25e3f2" stroke-width="8" />
<polygon points="30,130 140,130 70,200" fill="#25e302" />
<polygon points="70,130 190,130 130,200" style="fill:#25e302;stroke:#25e3f2;stroke-width:4" />
<polygon points="10,10 10,590 790,590 790,10" style="fill:none;stroke:#25e3f2;stroke-width:6" />
</svg>""" )
    
    #suppo.save( "shot-test.svg" )

def test_support_write():
    suppo= tll.SupportSVG()

    suppo.fillCircle( 250, 150, 2, 0xffe3f2 )
    suppo.write( 250, 150, "Hello", 0x25e3f2, 12 )
    suppo.write( 350, 250, "World", 0x25e3f2, 12 )
    suppo.write( 350, 260, "World", 0x25e3f2, 12 )
    suppo.write( 350, 270, "World", 0x25e3f2, 12 )
    suppo.write( 350, 280, "World", 0x25e3f2, 12 )

    print( "---\n" + suppo.render() )

    assert( suppo.render() == """<svg width="800" height="600">
<circle r="2" cx="250" cy="150" fill="#ffe3f2" />
<text x="250" y="150" fill="#25e3f2" font-family="Verdana" font-size="12">Hello</text>" />
<text x="350" y="250" fill="#25e3f2" font-family="Verdana" font-size="12">World</text>" />
<text x="350" y="260" fill="#25e3f2" font-family="Verdana" font-size="12">World</text>" />
<text x="350" y="270" fill="#25e3f2" font-family="Verdana" font-size="12">World</text>" />
<text x="350" y="280" fill="#25e3f2" font-family="Verdana" font-size="12">World</text>" />
</svg>""" )


def test_artist_load():
    pablo= tll.Artist()

    assert( type( pablo ) ) == tll.Artist
    assert( type( pablo.support() ) ) == tll.Support

    pablo.initializeSVG("shot-test.svg") 

    assert( type( pablo.support() ) ) == tll.SupportSVG

    print(pablo.render())
    assert( pablo.render() == """<svg width="800" height="600">
<polygon points="0,0 0,600 800,600 800,0" fill="#b86e00" />
</svg>""" )

    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    pablo.support().save( "shot-test.svg" )

    assert( pablo.render() == """<svg width="800" height="600">
<polygon points="0,0 0,600 800,600 800,0" fill="#b86e00" />
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
<circle r="6" cx="400.0" cy="300.0" fill="#0606e2" />
</svg>""" )


def test_artist_flip():
    shotImg= "shot-test.svg"
    pablo= tll.Artist().initializeSVG( filePath=shotImg )

    assert( pablo.support().filePath() == shotImg )

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/11.02-svg-flip-00.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/11.02-svg-flip-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/11.02-svg-flip-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    pablo.drawPolygon( [-1.26, -2.6, -0.4, 3.4], [-2.3, 0.3, 6, -1.7] )
    pablo.drawCircle( 1.26, 2.3, 3.2 )
    pablo.traceLine( -1.26, -2.3, 1.26, 2.3 )
    pablo.fillCircle( -1.26, -2.3, 0.2 )

    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/11.02-svg-flip-03.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )
