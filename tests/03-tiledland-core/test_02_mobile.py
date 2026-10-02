import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - M O B I L E
# ------------------------------------------------------------------------ #

def test_fast_mobile_init():
    entity= tild.Mobile()
    assert type(entity) == tild.Mobile

    assert type( entity.outline() ) == tild.geometry.Convex
    assert type( entity.shape() ) == tild.geometry.Convex

    points= [ str(p) for p in entity.outline().points() ]
    print( points )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    assert entity.orientation() == 0.0
    assert entity.position().asTuple() == (0.0, 0.0)

    bodyPoints= [ str(p) for p in entity.shape().points() ]
    assert points == bodyPoints


def test_fast_mobile_init2():
    entity= tild.Mobile()

    assert entity.enclave() == 0
    assert entity.index() == 0

    print( f"{entity.position()} == {Point(0.0, 0.0)}") 

    assert entity.position() == Point(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    
    print( env ) 
    assert env == [(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]

    entity.setOutline( tild.Convex().initRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    entity.setCoordinates(1.0, 2.0)
    assert entity.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]


def test_fast_mobile_init3():
    entity= tild.Mobile( tild.Convex().initRegular(0.5, 8) )
    entity.setColors(0xff6644, 0x991100, 4)
    entity.setPose( Point(1.0, 2.0), 0.4 )
    entity.setSelector( 12, 42 )

    assert entity.enclave() == 12
    assert entity.index() == 42
    assert entity.selector() == (12, 42)
    assert entity.position() == Point(1.0, 2.0)
    assert entity.orientation() == 0.4

    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.outline().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]
    
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.shape().asZipped() ]
    print( env )
    assert env == [(0.82, 1.82), (0.75, 2.0), (0.82, 2.18), (1.0, 2.25), (1.18, 2.18), (1.25, 2.0), (1.18, 1.82), (1.0, 1.75)]
    
def test_fast_mobile_transform():
    ent= tild.Mobile()
    ent.rotate( 1.67 )
    ent.translate( Point(1.5, -2.0) )

    artist= tild.artist.openSVG("shot-test.svg", 800, 600)
    artist.drawConvex( ent.outline(), tild.artist.palette01[3] )
    artist.drawConvex( ent.shape(), tild.artist.palette01[5] )
    artist.flip()
    
    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    points= [ str(p) for p in ent.outline().points() ]
    print( f"> reference : {points}" )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    bodyPoints= [ str(p) for p in ent.shape().points() ]
    print( f"> transfom  : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']

    ent.setPose( Point(0.0, 0.0), 0.0 )

    bodyPoints= [ str(p) for p in ent.shape().points() ]
    print( f"> return  : {bodyPoints}" )
    assert bodyPoints == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']

    ent.translate( Point(1.5, -2.0) )
    ent.rotate( 1.67 )

    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    bodyPoints= [ str(p) for p in ent.shape().points() ]
    print( f"> transfom2 : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']


def test_fast_mobile_draw():
    ent= tild.Mobile()
    ent.setColors(0x603800, 0xffcd80, 4)

    print(ent)

    tild.quickDraw(ent, "0", "shot-test.png", 800, 600)
    tild.quickDraw(ent, "0", "shot-test.svg", 800, 600)

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-mobile-draw-01.svg").read() )
    assert ent.position().asTuple() == (0.0, 0.0)
    assert ent.orientation() == 0.0

    shape= tild.Convex().initArrowTip(0.8)
    
    ent.setOutline(shape.copy())
    ent.rotate(2.2)
    ent.translate(Point(1.0, 0.6))

    shape.rotate(2.2)
    shape.translate(Point(1.0, 0.6))

    tild.quickDraw(ent, "0", "shot-test.png", 800, 600)
    tild.quickDraw(ent, "0", "shot-test.svg", 800, 600)

    assert shape.round(4).points() == ent.shape().round(4).points()

    assert ent.position().round(1).asTuple() == (1.0, 0.6)
    assert ent.orientation() == 2.2

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-mobile-draw-02.svg").read() )

def test_fast_mobile_str():
    entity= tild.Mobile( tild.Convex().initSquare(1.0))
    entity.setPosition( Point(1.0, 2.0) )
    entity.setSelector(12, 6)

    print(entity)
    assert str(entity) == "Mobile 12-6 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    entity= tild.Mobile( tild.Convex().initSquare(1.0) )
    entity.setCoordinates(1.0, 2.0)
    print(entity)
    assert str(entity) == "Mobile 0-0 ⌊(0.5, 1.5), (1.5, 2.5)⌉"
