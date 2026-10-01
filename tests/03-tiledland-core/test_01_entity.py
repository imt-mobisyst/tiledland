import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point


# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - E N T I T Y
# ------------------------------------------------------------------------ #

def test_fast_simpleent_init():
    ent= tild.SimpleEnt()
    assert type( ent ) == tild.SimpleEnt

    assert type( ent.shape() ) == tild.geometry.Convex
    assert ent.outline() is ent.shape()

    points= [ str(p) for p in ent.shape().points() ]
    print( points )
    assert points == ['(-0.5, -0.5)', '(-0.5, 0.5)', '(0.5, 0.5)', '(0.5, -0.5)']
    assert ent.position().asRoundTuple() == (0.0, 0.0)
    assert ent.orientation() == 0.0

def test_fast_simpleent_init2():
    entity= tild.SimpleEnt()

    print( f"{entity.position()} == {Point(0.0, 0.0)}") 
    assert entity.position() == Point(0.0, 0.0)
    
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    
    print( env ) 
    assert env == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]

    entity.setOutline( tild.Convex().initRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    entity.setPosition( Point(1.0, 2.0) )
    assert entity.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]

def test_fast_simpleent_init3():
    shape= tild.Convex().initRegular(0.5, 8)
    shape.rotate(0.4)
    shape.setCenter( Point(1.0, 2.0) )

    entity= tild.SimpleEnt( shape, 0xFF00FF00, 12, 42 )

    assert entity.position().round(4) == Point(1.0, 2.0)
    assert entity.orientation() == 0.0

    assert entity.enclave() == 12
    assert entity.index() == 42
    assert entity.selector() == (12, 42)

    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(0.82, 1.82), (0.75, 2.0), (0.82, 2.18), (1.0, 2.25), (1.18, 2.18), (1.25, 2.0), (1.18, 1.82), (1.0, 1.75)]
    
def test_fast_simpleEnt_transform():
    refShape= tild.Convex().initArrowTip(1.0).setCenter( tild.Point() )
    ent= tild.SimpleEnt( refShape.copy() )

    ent.setPose( Point(1.5, -2.0), 1.67 )

    artist= tild.artist.openPNG("shot-test.png", 800, 600)
    artist.drawConvex( refShape, tild.artist.palette.foreground[3] )
    artist.drawConvex( ent.shape(), tild.artist.palette.foreground[5] )
    artist.flip()

    assert ent.orientation() == 0.0
    assert ent.position().round(1) == Point(1.5, -2.0)

    points= refShape.asRoundZipped(2)
    print( "> reference : "+ str(points) )
    assert points == [(-0.47, -0.25), (-0.47, 0.25), (-0.03, 0.5), (0.47, 0.0), (-0.03, -0.5)]
    
    bodyPoints= ent.shape().asRoundZipped(2)
    print( f"> transfom  : {bodyPoints}" )
    assert bodyPoints == [(1.79, -2.43), (1.29, -2.48), (1.0, -2.07), (1.45, -1.52), (2.0, -1.97)]
    ent.setPose( Point(0.0, 0.0), 0.0 )

def test_fast_simpleEnt_str():
    entity= tild.SimpleEnt(tild.Convex())
    entity.shape().initSquare(1.0)
    entity.setPosition( Point(1.0, 2.0) )
    entity.setSelector(12, 6)

    print(entity)
    assert str(entity) == "SimpleEnt 12-6 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    entity= tild.SimpleEnt(tild.Convex().initSquare(1.0) )
    entity.setCoordinates(-1.0, 2.0)
    print(entity)
    assert str(entity) == "SimpleEnt 0-0 ⌊(-1.5, 1.5), (-0.5, 2.5)⌉"


def test_fast_SimpleEnt_draw():
    ent= tild.SimpleEnt( tild.Convex().initArrowTip(1.0) )
    ent.setCoordinates(0.0, 0.0)
    
    r, g, b= tild.color.decompose(0x80673A)
    print(f"color: {r} {r:02X}, {g} {g:02X}, {b} {b:02X}") 
    print(f"color: {tild.color.rgbColor( 0x80673A )}" )
    print(f"color: {tild.color.recompose(r, g, b):06X}") 
    print(f"color: {tild.color.lightest(0x80673A, 0.5):06X}") 
    print(f"color: {tild.color.darckest(0x80673A, 0.5):06X}") 

    assert ent.brush().fill == 0x000000
    assert ent.brush().stroke == 0x808080

    ent.setBrush(0x603800, 0xffcd80, 4)

    print(f"fill:   {ent.brush().fill:06X}") 
    print(f"stroke: {ent.brush().stroke:06X}") 

    print(f"{ent.brush().fill:08X}") 
    print(f"{ent.brush().stroke:08X}")

    assert ent.brush().fill == 0x603800
    assert ent.brush().stroke == 0xffcd80

    tild.drawSimpleEnt(ent, "0", "shot-test.svg", 800, 600)

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-entity-draw-01.svg").read() )

    assert ent.position().asTuple() == (0.0, 0.0)
    assert ent.orientation() == 0.0

    shape= tild.Convex().initArrowTip(0.8)
    shape.rotate(2.2)
    shape.translate( Point(1.0, 0.6) )

    print( f"{shape} - center: {shape.center().round(1).asTuple()}" )

    ent.setOutline( shape.copy() )
    print( f"{ent} ~ position: {ent.position().round(1).asTuple()}" )

    tild.drawSimpleEnt(ent, "0", "shot-test.svg", 800, 600)

    assert shape.asRoundZipped() == ent.shape().asRoundZipped()

    print( f"{ent} ~ position: {ent.position().round(1).asTuple()}" )

    assert ent.position().round(1).asTuple() == (1.0, 0.6)
    assert ent.orientation() == 0.0

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-entity-draw-02.svg").read() )
