import sys, pytest, math
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tild
from src.tiledland.geometry import Point


# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - S H A P E D
# ------------------------------------------------------------------------ #

def test_fast_shaped_init():
    shaped= tild.AbsShaped()

    assert type( shaped ) == tild.AbsShaped

    assert hasattr(shaped, "position")
    assert hasattr(shaped, "orientation")
    assert hasattr(shaped, "box")
    assert hasattr(shaped, "radius")
    assert hasattr(shaped, "shape")

    with pytest.raises(AssertionError) as exc_info:
        shaped.position()
    assert isinstance(exc_info.value, AssertionError)

    with pytest.raises(AssertionError) as exc_info:
        shaped.orientation()
    assert isinstance(exc_info.value, AssertionError)

    with pytest.raises(AssertionError) as exc_info:
        shaped.box()
    assert isinstance(exc_info.value, AssertionError)

    with pytest.raises(AssertionError) as exc_info:
        shaped.radius()
    assert isinstance(exc_info.value, AssertionError)

    with pytest.raises(AssertionError) as exc_info:
        shaped.shape()
    assert isinstance(exc_info.value, AssertionError)

    assert shaped.isValidShaped() == False

def test_fast_shaped_reactangle():
    rect= tild.Rectangle()

    assert type( rect ) == tild.Rectangle

    assert rect.position().asTuple() == (0.0, 0.0)
    assert rect.orientation() == 0.0
    assert str(rect.box()) == "⌊(-0.5, -0.5), (0.5, 0.5)⌉"
    assert rect.radius() ==  math.sqrt(0.5)
    assert str( rect.shape().asRoundZipped() ) == "[(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]"

    assert rect.isValidShaped()

    rect= tild.Rectangle(2.0, 1.0)
    rect.setPosition( Point(1.0, 0.0) )

    xy= rect.position()
    assert xy.asTuple() == (1.0, 0.0)
    
    theta= rect.orientation()
    assert theta == 0.0
    
    box= rect.box()
    assert str(box) ==  "⌊(0.0, -0.5), (2.0, 0.5)⌉"
    
    r= rect.radius()
    assert r ==  math.sqrt(1.25)

    conv= rect.shape()
    assert str( conv.asRoundZipped() ) == "[(0.0, -0.5), (0.0, 0.5), (2.0, 0.5), (2.0, -0.5)]"

    assert rect.isValidShaped()

    assert str(rect) == "Rectangle 0-0 ⌊(0.0, -0.5), (2.0, 0.5)⌉"

def test_fast_shaped_shaped():
    shaped= tild.Shaped()

    assert type( shaped ) == tild.Shaped

    assert shaped.position().asTuple() == (0.0, 0.0)
    assert shaped.orientation() == 0.0
    assert str(shaped.box()) == "⌊(-0.5, -0.5), (0.5, 0.5)⌉"
    assert shaped.radius() ==  math.sqrt(0.5)
    assert str( shaped.shape().asRoundZipped() ) == "[(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]"

    assert shaped.isValidShaped()

    assert shaped.owner() == 0
    assert shaped.category() == 0
    assert shaped.index() == 0

    shaped= tild.Shaped( tild.Convex().initSquare(2.0) )
    shaped.setPosition( Point(1.0, 0.0) )

    assert shaped.position().asTuple() == (1.0, 0.0)
    assert shaped.orientation() == 0.0
    assert str(shaped.box()) ==  "⌊(0.0, -1.0), (2.0, 1.0)⌉"
    assert shaped.radius() ==  math.sqrt(2)
    assert str( shaped.shape().asRoundZipped() ) == "[(0.0, -1.0), (0.0, 1.0), (2.0, 1.0), (2.0, -1.0)]"

    assert shaped.isValidShaped()

    assert str(shaped) == "Shaped 0-0 ⌊(0.0, -1.0), (2.0, 1.0)⌉"
