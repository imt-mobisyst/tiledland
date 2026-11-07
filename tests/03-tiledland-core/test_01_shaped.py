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
    assert hasattr(shaped, "convexhull")

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
        shaped.convexhull()
    assert isinstance(exc_info.value, AssertionError)

    assert shaped.isValidShaped() == False

def test_fast_reactangle_init():
    rect= tild.Rectangle()

    assert type( rect ) == tild.Rectangle

    xy= rect.position()
    assert xy.asTuple() == (0.0, 0.0)
    
    theta= rect.orientation()
    assert theta == 0.0
    
    box= rect.box()
    assert str(box) == "⌊(-0.5, -0.5), (0.5, 0.5)⌉"
    
    r= rect.radius()
    assert r ==  math.sqrt(0.5)

    conv= rect.convexhull()
    assert str( conv.asRoundZipped() ) == "[(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]"

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

    conv= rect.convexhull()
    assert str( conv.asRoundZipped() ) == "[(0.0, -0.5), (0.0, 0.5), (2.0, 0.5), (2.0, -0.5)]"

    assert rect.isValidShaped()
