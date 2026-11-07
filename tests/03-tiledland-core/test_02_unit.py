import sys, math
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - U N I T
# ------------------------------------------------------------------------ #

def test_fast_unit_init():
    unit= tild.Unit()
    assert type(unit) == tild.Unit

    assert unit.position().asTuple() == (0.0, 0.0)
    assert unit.orientation() == 0.0
    assert str(unit.box()) == "⌊(-0.5, -0.5), (0.5, 0.5)⌉"
    assert unit.radius() ==  math.sqrt(0.5)
    assert str( unit.shape().asRoundZipped() ) == "[(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]"

    assert unit.name() == "Unit"
    assert unit.isValidShaped()

    assert unit.owner() == 0
    assert unit.category() == 0
    assert unit.identifier() == 0

    assert type( unit.outline() ) == tild.geometry.Convex
    assert type( unit.shape() ) == tild.geometry.Convex

    assert not( unit.outline() is unit.shape() )

    points= [ str(p) for p in unit.outline().points() ]
    print( points )
    assert points == ['(-0.5, -0.5)', '(-0.5, 0.5)', '(0.5, 0.5)', '(0.5, -0.5)']
    
    assert unit.orientation() == 0.0
    assert unit.position().asTuple() == (0.0, 0.0)

    bodyPoints= [ str(p) for p in unit.shape().points() ]
    assert points == bodyPoints


def test_fast_unit_init2():
    unit= tild.Unit(
        tild.Convex().initArrowTip(1.0), Point(3.5, 2.0), 0.0,
        1, 2, 3
    )
    assert unit.position().asTuple() == (3.5, 2.0)
    assert unit.orientation() == 0.0
    assert str( unit.box() ) == "⌊(3.07, 1.5), (4.0, 2.5)⌉"
    assert round( unit.radius(), 1 ) ==  0.5

    assert str( unit.outline().asRoundZipped(2) ) == "[(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]"
    assert str( unit.shape().asRoundZipped(2) ) == "[(3.07, 1.75), (3.07, 2.25), (3.5, 2.5), (4.0, 2.0), (3.5, 1.5)]"

    assert unit.owner() == 1
    assert unit.category() == 2
    assert unit.identifier() == 3

    unit.setPosition( Point() )
    assert unit.position().asTuple() == (0.0, 0.0)
    assert str( unit.box() ) == "⌊(-0.43, -0.5), (0.5, 0.5)⌉"
    assert str( unit.outline().asRoundZipped(2) ) == "[(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]"
    assert str( unit.shape().asRoundZipped(2) ) == "[(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]"

    
def test_fast_mobile_transform():
    unit= tild.Unit( tild.Convex().initArrowTip(1.0) )
    unit.rotate( 1.67 )
    unit.translate( Point(1.5, -2.0) )

    artist= tild.artist.openPNG("shot-test.png", 800, 600)
    artist.drawConvex( unit.outline(), tild.artist.palettes[1][3] )
    artist.drawConvex( unit.shape(), tild.artist.palettes[1][5] )
    artist.flip()

    assert unit.orientation() == 1.67
    assert unit.position().asTuple() == (1.5, -2.0)

    points= [ str(p) for p in unit.outline().points() ]
    print( f"> reference : {points}" )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    bodyPoints= [ str(p) for p in unit.shape().points() ]
    print( f"> transfom  : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']

    unit.setPose( Point(0.0, 0.0), 0.0 )

    bodyPoints= [ str(p) for p in unit.shape().points() ]
    print( f"> return  : {bodyPoints}" )
    assert bodyPoints == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']

    unit.translate( Point(1.5, -2.0) )
    unit.rotate( 1.67 )

    assert unit.orientation() == 1.67
    assert unit.position().asTuple() == (1.5, -2.0)

    bodyPoints= [ str(p) for p in unit.shape().points() ]
    print( f"> transfom2 : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']

def test_fast_unit_draw():
    unit= tild.Unit( tild.Convex().initArrowTip(1.0), name="0" )
    
    assert unit.name() == "0"

    tild.drawUnit(unit, "shot-test.png", 800, 600)
    tild.drawUnit(unit, "shot-test.svg", 800, 600)

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-mobile-draw-01.svg").read() )
    assert unit.position().asTuple() == (0.0, 0.0)
    assert unit.orientation() == 0.0

    shape= tild.Convex().initArrowTip(0.8)
    
    unit.setOutline(shape.copy())
    unit.rotate(2.2)
    unit.translate(Point(1.0, 0.6))

    shape.rotate(2.2)
    shape.translate(Point(1.0, 0.6))

    tild.drawUnit( unit, "shot-test.png", 800, 600 )
    tild.drawUnit( unit, "shot-test.svg", 800, 600 )

    assert shape.round(4).points() == unit.shape().round(4).points()

    assert unit.position().round(1).asTuple() == (1.0, 0.6)
    assert unit.orientation() == 2.2

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-mobile-draw-02.svg").read() )

def test_fast_unit_str():
    unit= tild.Unit( tild.Convex().initSquare(1.0),
        owner=1, category= 2, identifier=3 )
    unit.setPosition( Point(1.0, 2.0) )

    print(unit)
    assert str(unit) == "Unit 1-3 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    unit= tild.Unit( tild.Convex().initSquare(1.0), Point(1.0, 2.0) )
    print(unit)
    assert str(unit) == "Unit 0-0 ⌊(0.5, 1.5), (1.5, 2.5)⌉"
